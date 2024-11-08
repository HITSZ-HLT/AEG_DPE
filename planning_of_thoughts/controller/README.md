# Controller

The Controller class is responsible for traversing the Graph of Operations (GoO), which is a static structure that is constructed once, before the execution starts.
GoO prescribes the execution plan of thought operations and the Controller invokes their execution, generating the Graph Reasoning State (GRS).

In order for a GoO to be executed, an instance of Large Language Model (LLM) must be supplied to the controller.
Currently, the framework supports the following LLMs:

- GPT-4 / GPT-3.5 (Remote - OpenAI API)
- Llama-2 (Local - HuggingFace Transformers)

The following section describes how to instantiate individual LLMs and the Controller to run a defined GoO.
Furthermore, the process of adding new LLMs into the framework is outlined at the end.

## LLM Instantiation

- Create a copy of `config_template.json` named `config.json`.
- Fill configuration details based on the used model (below).

### GPT-4 / GPT-3.5

- Adjust predefined `chatgpt`, `chatgpt4` or create new configuration with an unique key.

| Key                 | Value                                                                                                                                                                                                                                                                                                                                                               |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| model_id            | Model name based on [OpenAI model overview](https://platform.openai.com/docs/models/overview).                                                                                                                                                                                                                                                                      |
| prompt_token_cost   | Price per 1000 prompt tokens based on [OpenAI pricing](https://openai.com/pricing), used for calculating cumulative price per LLM instance.                                                                                                                                                                                                                         |
| response_token_cost | Price per 1000 response tokens based on [OpenAI pricing](https://openai.com/pricing), used for calculating cumulative price per LLM instance.                                                                                                                                                                                                                       |
| temperature         | Parameter of OpenAI models that controls randomness and the creativity of the responses (higher temperature = more diverse and unexpected responses). Value between 0.0 and 2.0, default is 1.0. More information can be found in the [OpenAI API reference](https://platform.openai.com/docs/api-reference/completions/create#completions/create-temperature).     |
| max_tokens          | The maximum number of tokens to generate in the chat completion. Value depends on the maximum context size of the model specified in the [OpenAI model overview](https://platform.openai.com/docs/models/overview). More information can be found in the [OpenAI API reference](https://platform.openai.com/docs/api-reference/chat/create#chat/create-max_tokens). |
| stop                | String or array of strings specifying sequence of characters which if detected, stops further generation of tokens. More information can be found in the [OpenAI API reference](https://platform.openai.com/docs/api-reference/chat/create#chat/create-stop).                                                                                                       |
| organization        | Organization to use for the API requests (may be empty).                                                                                                                                                                                                                                                                                                            |
| api_key             | Personal API key that will be used to access OpenAI API.                                                                                                                                                                                                                                                                                                            |

- Instantiate the language model based on the selected configuration key (predefined / custom).

```
lm = controller.ChatGPT(
    "path/to/config.json",
    model_name=<configuration key>
)
```

### Llama-2

- Requires local hardware to run inference and a HuggingFace account.
- Adjust predefined `llama7b-hf`, `llama13b-hf`, `llama70b-hf` or create a new configuration with an unique key.

| Key                 | Value                                                                                                                                                                           |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| model_id            | Specifies HuggingFace Llama 2 model identifier (`meta-llama/<model_id>`).                                                                                                       |
| cache_dir           | Local directory where model will be downloaded and accessed.                                                                                                                    |
| prompt_token_cost   | Price per 1000 prompt tokens (currently not used - local model = no cost).                                                                                                      |
| response_token_cost | Price per 1000 response tokens (currently not used - local model = no cost).                                                                                                    |
| temperature         | Parameter that controls randomness and the creativity of the responses (higher temperature = more diverse and unexpected responses). Value between 0.0 and 1.0, default is 0.6. |
| top_k               | Top-K sampling method described in [Transformers tutorial](https://huggingface.co/blog/how-to-generate). Default value is set to 10.                                            |
| max_tokens          | The maximum number of tokens to generate in the chat completion. More tokens require more memory.                                                                               |

- Instantiate the language model based on the selected configuration key (predefined / custom).

```
lm = controller.Llama2HF(
    "path/to/config.json",
    model_name=<configuration key>
)
```

- Request access to Llama-2 via the [Meta form](https://ai.meta.com/resources/models-and-libraries/llama-downloads/) using the same email address as for the HuggingFace account.
- After the access is granted, go to [HuggingFace Llama-2 model card](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf), log in and accept the license (_"You have been granted access to this model"_ message should appear).
- Generate HuggingFace access token.
- Log in from CLI with: `huggingface-cli login --token <your token>`.

Note: 4-bit quantization is used to reduce the model size for inference. During instantiation, the model is downloaded from HuggingFace into the cache directory specified in the `config.json`. Running queries using larger models will require multiple GPUs (splitting across many GPUs is done automatically by the Transformers library).

## Controller Instantiation

- Requires custom `Prompter`, `Parser` and instantiated `GraphOfOperations` - creation of these is described separately.
- Use instantiated `lm` from above.
- Prepare initial state (thought) as dictionary - this can be used in the initial prompts by the operations.

```
graph_of_operations = ...create

executor = controller.Controller(
    lm,
    graph_of_operations,
    <CustomPrompter()>,
    <CustomParser()>,
    <initial state>,
)
executor.run()
executor.output_graph("path/to/output.json")
```

- After the run the graph is written to an output file, which contains individual operations, their thoughts, information about scores and validity and total amount of used tokens / cost.

## Adding LLMs

More LLMs can be added by following these steps:

- Create new class as a subclass of `AbstractLanguageModel`.
- Use the constructor for loading configuration and instantiating the language model (if needed).

```
class CustomLanguageModel(AbstractLanguageModel):
    def __init__(
        self,
        config_path: str = "",
        model_name: str = "llama7b-hf",
        cache: bool = False
    ) -> None:
        super().__init__(config_path, model_name, cache)
        self.config: Dict = self.config[model_name]

        # Load data from configuration into variables if needed

        # Instantiate LLM if needed
```

- Implement `query` abstract method that is used to get a list of responses from the LLM (call to remote API or local model inference).

```
def query(self, query: str, num_responses: int = 1) -> Any:
    # Support caching
    # Call LLM and retrieve list of responses - based on num_responses
    # Return LLM response structure (not only raw strings)
```

- Implement `get_response_texts` abstract method that is used to get a list of raw texts from the LLM response structure produced by `query`.

```
def get_response_texts(self, query_response: Union[List[Dict], Dict]) -> List[str]:
    # Retrieve list of raw strings from the LLM response structure
```

自我介绍：何宇航，本科毕业于华南理工大学，硕士就读于哈尔滨工业大学，研究方向是自然语言处理、论辩挖掘和生成、大模型应用，期间曾获得过国家奖学金、三好学生、特等奖学金等。参加过 CCAC 智慧论辩竞赛获得第一名。就读期间以第一作者/共同第一作者发表 3 篇论文至 EMNLP、DASFAA、中文信息学报。

class GenerationConfig(PushToHubMixin):
r"""
Class that holds a configuration for a generation task. A `generate` call supports the following generation methods
for text-decoder, text-to-text, speech-to-text, and vision-to-text models:

        - *greedy decoding* by calling [`~generation.GenerationMixin.greedy_search`] if `num_beams=1` and
            `do_sample=False`
        - *contrastive search* by calling [`~generation.GenerationMixin.contrastive_search`] if `penalty_alpha>0.`
            and `top_k>1`
        - *multinomial sampling* by calling [`~generation.GenerationMixin.sample`] if `num_beams=1` and
            `do_sample=True`
        - *beam-search decoding* by calling [`~generation.GenerationMixin.beam_search`] if `num_beams>1` and
            `do_sample=False`
        - *beam-search multinomial sampling* by calling [`~generation.GenerationMixin.beam_sample`] if
            `num_beams>1` and `do_sample=True`
        - *diverse beam-search decoding* by calling [`~generation.GenerationMixin.group_beam_search`], if
            `num_beams>1` and `num_beam_groups>1`
        - *constrained beam-search decoding* by calling [`~generation.GenerationMixin.constrained_beam_search`], if
            `constraints!=None` or `force_words_ids!=None`
        - *assisted decoding* by calling [`~generation.GenerationMixin.assisted_decoding`], if
            `assistant_model` is passed to `.generate()`

    You do not need to call any of the above methods directly. Pass custom parameter values to '.generate()'. To learn
    more about decoding strategies refer to the [text generation strategies guide](../generation_strategies).

    Arg:
        > Parameters that control the length of the output

        max_length (`int`, *optional*, defaults to 20):
            The maximum length the generated tokens can have. Corresponds to the length of the input prompt +
            `max_new_tokens`. Its effect is overridden by `max_new_tokens`, if also set.
        max_new_tokens (`int`, *optional*):
            The maximum numbers of tokens to generate, ignoring the number of tokens in the prompt.
        min_length (`int`, *optional*, defaults to 0):
            The minimum length of the sequence to be generated. Corresponds to the length of the input prompt +
            `min_new_tokens`. Its effect is overridden by `min_new_tokens`, if also set.
        min_new_tokens (`int`, *optional*):
            The minimum numbers of tokens to generate, ignoring the number of tokens in the prompt.
        early_stopping (`bool` or `str`, *optional*, defaults to `False`):
            Controls the stopping condition for beam-based methods, like beam-search. It accepts the following values:
            `True`, where the generation stops as soon as there are `num_beams` complete candidates; `False`, where an
            heuristic is applied and the generation stops when is it very unlikely to find better candidates;
            `"never"`, where the beam search procedure only stops when there cannot be better candidates (canonical
            beam search algorithm).
        max_time(`float`, *optional*):
            The maximum amount of time you allow the computation to run for in seconds. generation will still finish
            the current pass after allocated time has been passed.

        > Parameters that control the generation strategy used

        do_sample (`bool`, *optional*, defaults to `False`):
            Whether or not to use sampling ; use greedy decoding otherwise.
        num_beams (`int`, *optional*, defaults to 1):
            Number of beams for beam search. 1 means no beam search.
        num_beam_groups (`int`, *optional*, defaults to 1):
            Number of groups to divide `num_beams` into in order to ensure diversity among different groups of beams.
            [this paper](https://arxiv.org/pdf/1610.02424.pdf) for more details.
        penalty_alpha (`float`, *optional*):
            The values balance the model confidence and the degeneration penalty in contrastive search decoding.
        use_cache (`bool`, *optional*, defaults to `True`):
            Whether or not the model should use the past last key/values attentions (if applicable to the model) to
            speed up decoding.

        > Parameters for manipulation of the model output logits

        temperature (`float`, *optional*, defaults to 1.0):
            The value used to modulate the next token probabilities.
        top_k (`int`, *optional*, defaults to 50):
            The number of highest probability vocabulary tokens to keep for top-k-filtering.
        top_p (`float`, *optional*, defaults to 1.0):
            If set to float < 1, only the smallest set of most probable tokens with probabilities that add up to
            `top_p` or higher are kept for generation.
        typical_p (`float`, *optional*, defaults to 1.0):
            Local typicality measures how similar the conditional probability of predicting a target token next is to
            the expected conditional probability of predicting a random token next, given the partial text already
            generated. If set to float < 1, the smallest set of the most locally typical tokens with probabilities that
            add up to `typical_p` or higher are kept for generation. See [this
            paper](https://arxiv.org/pdf/2202.00666.pdf) for more details.
        epsilon_cutoff (`float`, *optional*, defaults to 0.0):
            If set to float strictly between 0 and 1, only tokens with a conditional probability greater than
            `epsilon_cutoff` will be sampled. In the paper, suggested values range from 3e-4 to 9e-4, depending on the
            size of the model. See [Truncation Sampling as Language Model
            Desmoothing](https://arxiv.org/abs/2210.15191) for more details.
        eta_cutoff (`float`, *optional*, defaults to 0.0):
            Eta sampling is a hybrid of locally typical sampling and epsilon sampling. If set to float strictly between
            0 and 1, a token is only considered if it is greater than either `eta_cutoff` or `sqrt(eta_cutoff) *
            exp(-entropy(softmax(next_token_logits)))`. The latter term is intuitively the expected next token
            probability, scaled by `sqrt(eta_cutoff)`. In the paper, suggested values range from 3e-4 to 2e-3,
            depending on the size of the model. See [Truncation Sampling as Language Model
            Desmoothing](https://arxiv.org/abs/2210.15191) for more details.
        diversity_penalty (`float`, *optional*, defaults to 0.0):
            This value is subtracted from a beam's score if it generates a token same as any beam from other group at a
            particular time. Note that `diversity_penalty` is only effective if `group beam search` is enabled.
        repetition_penalty (`float`, *optional*, defaults to 1.0):
            The parameter for repetition penalty. 1.0 means no penalty. See [this
            paper](https://arxiv.org/pdf/1909.05858.pdf) for more details.
        encoder_repetition_penalty (`float`, *optional*, defaults to 1.0):
            The paramater for encoder_repetition_penalty. An exponential penalty on sequences that are not in the
            original input. 1.0 means no penalty.
        length_penalty (`float`, *optional*, defaults to 1.0):
            Exponential penalty to the length that is used with beam-based generation. It is applied as an exponent to
            the sequence length, which in turn is used to divide the score of the sequence. Since the score is the log
            likelihood of the sequence (i.e. negative), `length_penalty` > 0.0 promotes longer sequences, while
            `length_penalty` < 0.0 encourages shorter sequences.
        no_repeat_ngram_size (`int`, *optional*, defaults to 0):
            If set to int > 0, all ngrams of that size can only occur once.
        bad_words_ids(`List[List[int]]`, *optional*):
            List of token ids that are not allowed to be generated. In order to get the token ids of the words that
            should not appear in the generated text, use `tokenizer(bad_words, add_prefix_space=True,
            add_special_tokens=False).input_ids`.
        force_words_ids(`List[List[int]]` or `List[List[List[int]]]`, *optional*):
            List of token ids that must be generated. If given a `List[List[int]]`, this is treated as a simple list of
            words that must be included, the opposite to `bad_words_ids`. If given `List[List[List[int]]]`, this
            triggers a [disjunctive constraint](https://github.com/huggingface/transformers/issues/14081), where one
            can allow different forms of each word.
        renormalize_logits (`bool`, *optional*, defaults to `False`):
            Whether to renormalize the logits after applying all the logits processors or warpers (including the custom
            ones). It's highly recommended to set this flag to `True` as the search algorithms suppose the score logits
            are normalized but some logit processors or warpers break the normalization.
        constraints (`List[Constraint]`, *optional*):
            Custom constraints that can be added to the generation to ensure that the output will contain the use of
            certain tokens as defined by `Constraint` objects, in the most sensible way possible.
        forced_bos_token_id (`int`, *optional*, defaults to `model.config.forced_bos_token_id`):
            The id of the token to force as the first generated token after the `decoder_start_token_id`. Useful for
            multilingual models like [mBART](../model_doc/mbart) where the first generated token needs to be the target
            language token.
        forced_eos_token_id (`Union[int, List[int]]`, *optional*, defaults to `model.config.forced_eos_token_id`):
            The id of the token to force as the last generated token when `max_length` is reached. Optionally, use a
            list to set multiple *end-of-sequence* tokens.
        remove_invalid_values (`bool`, *optional*, defaults to `model.config.remove_invalid_values`):
            Whether to remove possible *nan* and *inf* outputs of the model to prevent the generation method to crash.
            Note that using `remove_invalid_values` can slow down generation.
        exponential_decay_length_penalty (`tuple(int, float)`, *optional*):
            This Tuple adds an exponentially increasing length penalty, after a certain amount of tokens have been
            generated. The tuple shall consist of: `(start_index, decay_factor)` where `start_index` indicates where
            penalty starts and `decay_factor` represents the factor of exponential decay
        suppress_tokens  (`List[int]`, *optional*):
            A list of tokens that will be suppressed at generation. The `SupressTokens` logit processor will set their
            log probs to `-inf` so that they are not sampled.
        begin_suppress_tokens  (`List[int]`, *optional*):
            A list of tokens that will be suppressed at the beginning of the generation. The `SupressBeginTokens` logit
            processor will set their log probs to `-inf` so that they are not sampled.
        forced_decoder_ids (`List[List[int]]`, *optional*):
            A list of pairs of integers which indicates a mapping from generation indices to token indices that will be
            forced before sampling. For example, `[[1, 123]]` means the second generated token will always be a token
            of index 123.

        > Parameters that define the output variables of `generate`

        num_return_sequences(`int`, *optional*, defaults to 1):
            The number of independently computed returned sequences for each element in the batch.
        output_attentions (`bool`, *optional*, defaults to `False`):
            Whether or not to return the attentions tensors of all attention layers. See `attentions` under returned
            tensors for more details.
        output_hidden_states (`bool`, *optional*, defaults to `False`):
            Whether or not to return the hidden states of all layers. See `hidden_states` under returned tensors for
            more details.
        output_scores (`bool`, *optional*, defaults to `False`):
            Whether or not to return the prediction scores. See `scores` under returned tensors for more details.
        return_dict_in_generate (`bool`, *optional*, defaults to `False`):
            Whether or not to return a [`~utils.ModelOutput`] instead of a plain tuple.

        > Special tokens that can be used at generation time

        pad_token_id (`int`, *optional*):
            The id of the *padding* token.
        bos_token_id (`int`, *optional*):
            The id of the *beginning-of-sequence* token.
        eos_token_id (`Union[int, List[int]]`, *optional*):
            The id of the *end-of-sequence* token. Optionally, use a list to set multiple *end-of-sequence* tokens.

        > Generation parameters exclusive to encoder-decoder models

        encoder_no_repeat_ngram_size (`int`, *optional*, defaults to 0):
            If set to int > 0, all ngrams of that size that occur in the `encoder_input_ids` cannot occur in the
            `decoder_input_ids`.
        decoder_start_token_id (`int`, *optional*):
            If an encoder-decoder model starts decoding with a different token than *bos*, the id of that token.

        > Wild card

        generation_kwargs:
            Additional generation kwargs will be forwarded to the `generate` function of the model. Kwargs that are not
            present in `generate`'s signature will be used in the model forward pass.
    """
