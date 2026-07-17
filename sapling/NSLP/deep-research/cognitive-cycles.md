# Cognitive Cycle Algorithms — Canonical Research

> **Knowledge base for the S.E.E.D.
> cognitive cycle**. Algorithms that
> govern the 12-phase C cycle, prediction,
> memory consolidation, attention, and
> reinforcement learning. Each entry is
> sourced to its canonical reference and
> profiled for SXL integration.
>
> **Status (2026-07-16)**: 24 algorithms
> profiled. 16 are flagged
> `ready-for-promotion`.

## 1. Working Memory and Attention

### 1.1 ACT-R Declarative Memory Activation

- **Year / citation**: Anderson 1993 (*The Adaptive Character
  of Thought*); Anderson 2007 (*How Can the Human Mind
  Occur in a Physical System?*). Pievot, Anderson et al.
  (2005+ ACT-R reference papers).
- **Core idea**: The activation of a chunk i in declarative
  memory is
  `A_i = ln(Σ_j t_j^(-d)) + Σ_k W_k · S_ik + ε`,
  where t_j is the time since the jth presentation, d is the
  decay parameter (default 0.5), W_k are the strengths of
  the elements in the current goal/context, and S_ik is the
  similarity between element k and the i-th chunk. ε is a
  noise term.
- **Community status**: Active research community (act-r.psy.cmu.edu);
  textbook in cognitive psychology and AI.
- **Complexity**: O(N) per retrieval; N = number of chunks.
- **Pseudocode**:
  ```lisp
  (define (actr-activation chunk context d)
    (let ((base-level (log (sum (map (lambda (t) (expt t (- d)))
                                (access-times chunk)))))
          (spreading  (sum (map (lambda (k)
                                  (* (weight k) (similarity k chunk)))
                                context-elements))))
      (+ base-level spreading (random-noise))))
  ```
- **Worked example**: chunk A has been accessed at t=[1, 2, 5]
  seconds; d=0.5. base_level = ln(1^(-0.5) + 2^(-0.5) + 5^(-0.5))
  = ln(1 + 0.707 + 0.447) = ln(2.154) = 0.767. With one
  matching context element (W=1, S=0.9) and ε=0,
  A = 0.767 + 0.9 = 1.667. Retrieval probability over a
  threshold is sigmoid(1.667 - τ) where τ is the retrieval
  threshold.
- **Canonical reference**: https://act-r.psy.cmu.edu/
- **SXL shape**:
  ```lisp
  (:type actr-retrieval :schema "seed.cog/actr/v1"
   :content (:chunk-id "..." :context [{:element "..." :weight ... :similarity ...}]
             :d 0.5 :epsilon 0.0 :activation 1.667 :threshold 0.5))
  ```
- **Confirmation flag**: 🟢 `confirmed-curated`
- **Ready-for-promotion**: ✅ Yes.

### 1.2 SOAR Decision Cycle

- **Year / citation**: Laird 2012 (book: *The Soar Cognitive
  Architecture*). Laird, Newell, Rosenbloom 1987 (Soar paper).
- **Core idea**: Each cycle selects one operator via
  preference-based elaboration + decision. If the decision is
  *impasse* (ties, no candidates, etc.) SOAR recursively
  generates a sub-state to resolve it; the result becomes a
  *chunk* (compiled production) for future use.
- **Community status**: The Soar cognitive architecture is in
  continuous development; the chunking mechanism is the
  canonical model of skill acquisition.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 1.3 Global Workspace Theory (GWT) and the Neuronal Global Workspace

- **Year / citation**: Baars 1988 (*A Cognitive Theory of
  Consciousness*). Dehaene 2014 (*Consciousness and the
  Brain*).
- **Core idea**: Many specialised modules compete for access
  to a *global workspace*; the winning coalition is
  *broadcast* to all modules. Conscious access corresponds
  to global ignition (Dehaene's neural correlate).
- **Community status**: Major theory of consciousness; many
  cognitive architectures implement GWT.
- **SXL shape**: A workspace is an SXL entity
  `(:type workspace :id ... :content {:coalition [...]:modules [...] :broadcast-epoch 0 ...})`.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 1.4 Soft Attention (Bahdanau)

- **Year / citation**: Bahdanau, Cho, Bengio 2014. "Neural
  Machine Translation by Jointly Learning to Align and
  Translate". arXiv:1409.0473.
- **Core idea**: A context vector c_i = Σ_j α_ij h_j where
  α_ij = softmax(e_ij) and e_ij = a(s_{i-1}, h_j) is a
  learned alignment score.
- **Complexity**: O(L²) for sequence length L.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes (universal).

### 1.5 Multi-Head Self-Attention / Transformer

- **Year / citation**: Vaswani et al. 2017. "Attention Is All
  You Need". NeurIPS 2017.
- **Core idea**: `MultiHead(Q, K, V) = Concat(head_1, ..., head_h) W^O`,
  where `head_i = Attention(Q W^Q_i, K W^K_i, V W^V_i)` and
  `Attention(Q, K, V) = softmax(Q K^T / √d_k) V`.
- **Complexity**: O(L²) per layer in sequence length L.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 1.6 Squeeze-and-Excitation (channel attention)

- **Year / citation**: Hu, Shen, Sun 2018. "Squeeze-and-
  Excitation Networks". CVPR 2018.
- **Core idea**: Global average pooling → FC → ReLU → FC →
  sigmoid → channel-wise multiplication. Recalibrates channel
  responses.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 1.7 Itti-Koch-Niebur Saliency Map

- **Year / citation**: Itti, Koch, Niebur 1998. "A Model of
  Saliency-Based Visual Attention". *IEEE TPAMI* 20(11):
  1254–1259.
- **Core idea**: Linear combination of feature maps
  (intensity, colour, orientation) at multiple scales,
  followed by centre-surround differences and
  across-scale combination.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

## 2. Prediction and Prediction Error

### 2.1 Kalman Filter

- **Year / citation**: Kalman 1960 (see Part 1 of
  sxl-operators.md).
- **Core idea**: Linear-Gaussian state-space model. The
  predict step is `x̂_{k|k-1} = F x̂_{k-1|k-1}` and
  `P_{k|k-1} = F P_{k-1|k-1} F^T + Q`; the update step is
  `K_k = P_{k|k-1} H^T (H P_{k|k-1} H^T + R)^{-1}`,
  `x̂_{k|k} = x̂_{k|k-1} + K_k (z_k - H x̂_{k|k-1})`,
  `P_{k|k} = (I - K_k H) P_{k|k-1}`.
- **Worked example**: A robot with state [x, ẋ]ᵀ. Predict
  with F = [[1, 1], [0, 1]]. If P = [[1, 0], [0, 1]],
  Q = [[0.1, 0], [0, 0.1]], then P_{k|k-1} = F P F^T + Q =
  [[2.1, 1.0], [1.0, 1.1]]. With H = [1, 0], R = 0.5,
  K = [2.1, 1.0]^T (3.1)^{-1} = [0.677, 0.323]^T.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 2.2 Extended Kalman Filter (EKF)

- **Year / citation**: Smith, Schmidt, McGee 1962 (first
  application); Jazwinski 1970 (book).
- **Core idea**: Linearises non-linear transition and
  observation models about the current estimate with first-
  order Taylor expansion.
- **Confirmation flag**: 🟢 `confirmed-curated`
- **Ready-for-promotion**: ✅ Yes.

### 2.3 Particle Filter

- **Year / citation**: Gordon, Salmond, Smith 1993 (see
  sxl-operators.md).
- **Worked example**: N=1000 particles, each with weight
  w_i ∝ p(z_k | x_i). Resample with replacement proportional
  to w_i. Effective sample size N_eff = 1 / Σ w_i²; resample
  when N_eff < N/2.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 2.4 Bayesian Surprise (Itti-Baldi)

- **Year / citation**: Itti & Baldi 2006. "Bayesian Surprise
  Attracts Human Attention". *Vision Research* 46(8-9):
  1295–1315.
- **Core idea**: Surprise is the KL divergence between the
  prior and posterior beliefs about the world: `S = KL(p(θ|D) ‖ p(θ))`.
- **Confirmation flag**: 🟢 `confirmed-curated`
- **Ready-for-promotion**: ✅ Yes.

### 2.5 Free-Energy Principle / Active Inference

- **Year / citation**: Friston 2010. "The Free-Energy
  Principle: A Unified Brain Theory?" *Nature Reviews
  Neuroscience* 11: 127–138. Friston, FitzGerald, Rigoli,
  Schwartenbeck, Pezzulo 2017. "Active Inference: A Process
  Theory". *Neural Computation* 29: 1–49.
- **Core idea**: The brain minimises variational free energy
  F = -E_q[ln p(o,s)] - H[q(s)] as an upper bound on -ln p(o).
  Active inference adds action that minimises expected free
  energy.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 2.6 Predictive Coding (Rao-Ballard)

- **Year / citation**: Rao & Ballard 1999. "Predictive Coding
  in the Visual Cortex". *Nature Neuroscience* 2: 79–87.
- **Core idea**: Hierarchical cortical areas minimise
  prediction error at each level by adjusting predictions
  via top-down connections. The free-energy framework
  subsumes it.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 2.7 Hidden Markov Model and Baum-Welch

- **Year / citation**: Baum & Petrie 1966. Viterbi 1967
  (decoding); Baum 1972 (EM algorithm for HMMs).
- **Core idea**: Three classical problems:
  - *Likelihood*: forward algorithm O(T N²).
  - *Decoding*: Viterbi O(T N²).
  - *Learning*: Baum-Welch (EM) O(T N²) per iteration.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

## 3. Memory Consolidation

### 3.1 Ebbinghaus Forgetting Curve

- **Year / citation**: Ebbinghaus 1885 (*Über das
  Gedächtnis*). Translated 1913.
- **Core idea**: Retention R(t) = exp(-t/S) where S is the
  memory strength (depends on rehearsal). Modern variant:
  R(t) = (1 + t/S)^(-β) with β ≈ 0.5 (Wixted & Carpenter
  2007).
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 3.2 Power Law of Practice

- **Year / citation**: Newell & Rosenbloom 1981. "Mechanisms
  of Skill Acquisition and the Law of Practice". In
  *Anderson 1981 Cognitive Skills and Their Acquisition*.
- **Core idea**: Time to perform a task T(n) = a + b n^(-c)
  where n is the number of practice trials and c ≈ 0.4-0.6.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 3.3 Synaptic Tagging and Capture (STC)

- **Year / citation**: Frey & Morris 1997. "Synaptic Tagging
  and Long-Term Potentiation". *Nature* 385: 533–536.
- **Core idea**: Weak stimulation sets a *synaptic tag*
  that lasts ~1-3 hours. Strong stimulation within that
  window releases *plasticity-related proteins* (PRPs) that
  "capture" the tagged synapse, converting early-LTP to
  late-LTP.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 3.4 Complementary Learning Systems (CLS)

- **Year / citation**: McClelland, McNaughton, O'Reilly 1995.
  "Why There Are Complementary Learning Systems in the
  Hippocampus and Neocortex". *Psychological Review* 102(3):
  419–457.
- **Core idea**: The hippocampus is a fast, low-capacity
  store for recent episodes; the neocortex is a slow,
  high-capacity store for semantic knowledge. Off-line
  replay (during sleep) transfers knowledge from the
  hippocampus to the neocortex.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 3.5 Hippocampal Replay (Sharp-Wave Ripples)

- **Year / citation**: Wilson & McNaughton 1994. "Reactivation
  of Hippocampal Neuronal Ensembles During Sleep". *Science*
  265: 676–679. Buzsáki 1989. "Two-stage model of memory
  trace formation: a role for 'noisy' brain states".
  *Neuroscience* 31(3): 551–570.
- **Core idea**: During slow-wave sleep and quiet
  wakefulness, place-cell firing sequences from prior
  experience are *replayed* in compressed time (10-20×) on
  sharp-wave ripples (~200 Hz). The replay is the substrate
  of systems consolidation.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 3.6 Memory Reconsolidation

- **Year / citation**: Nader, Schafe, Le Doux 2000. "The
  Labile Nature of Consolidation Theory". *Nature Reviews
  Neuroscience* 1: 216–219.
- **Core idea**: Reactivation of a consolidated memory
  returns it to a labile state, after which it must be
  reconsolidated. The reconsolidation window is ~6 hours.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 3.7 Schema Consolidation

- **Year / citation**: Gilboa & Marlatte 2017. "Neurobiology
  of Schemas and Schema-Mediated Memory". *Trends in
  Cognitive Sciences* 21(8): 618–631.
- **Core idea**: Existing schemata facilitate consolidation
  of new related memories (the *schema effect*).
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

## 4. Learning Algorithms

### 4.1 Hebbian Learning

- **Year / citation**: Hebb 1949 (*The Organization of
  Behavior*).
- **Core idea**: "When an axon of cell A is near enough to
  excite cell B and repeatedly or persistently takes part in
  firing it, some growth process or metabolic change takes
  place in one or both cells…". Formally Δw_{ij} = η x_i x_j.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 4.2 Oja's Rule

- **Year / citation**: Oja 1982. "Simplified Neuron Model as
  a Principal Component Analyzer". *J. Math. Biol.* 15:
  267–273.
- **Core idea**: A normalised Hebbian rule: Δw = η (y x -
  y² w). Converges to the first principal component of the
  input covariance.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 4.3 STDP (Spike-Timing-Dependent Plasticity)

- **Year / citation**: Bi & Poo 1998. "Synaptic Modifications
  in Cultured Hippocampal Neurons". *J. Neurosci.* 18(24):
  10464–10472.
- **Core idea**: Δw = A_+ exp(-Δt/τ_+) for Δt > 0 (LTP);
  Δw = -A_- exp(Δt/τ_-) for Δt < 0 (LTD). With A_+, A_-,
  τ_+, τ_- measured from data.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 4.4 Backpropagation

- **Year / citation**: Rumelhart, Hinton, Williams 1986.
  "Learning Representations by Back-Propagating Errors".
  *Nature* 323: 533–536.
- **Core idea**: Chain rule through the computation graph.
  Computes ∂L/∂W layer-by-layer from the output error.
- **Complexity**: O(N) per example for an N-parameter
  network.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 4.5 Adam Optimiser

- **Year / citation**: Kingma & Ba 2014. "Adam: A Method for
  Stochastic Optimization". arXiv:1412.6980.
- **Core idea**: Per-parameter learning rate from estimates
  of first and second moments of the gradient:
  m_t = β_1 m_{t-1} + (1-β_1) g_t,
  v_t = β_2 v_{t-1} + (1-β_2) g_t²,
  θ_t = θ_{t-1} - η m̂_t / (√v̂_t + ε).
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 4.6 Elastic Weight Consolidation (EWC)

- **Year / citation**: Kirkpatrick et al. 2017. "Overcoming
  Catastrophic Forgetting in Neural Networks". *PNAS* 114(13):
  3521–3526.
- **Core idea**: Add a quadratic regulariser that penalises
  changes to parameters weighted by the diagonal of the
  Fisher information matrix: L = L_task + λ Σ_i F_ii (θ_i -
  θ*_i)².
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 4.7 Synaptic Intelligence (SI)

- **Year / citation**: Zenke, Poole, Ganguli 2017.
  "Continual Learning Through Synaptic Intelligence". ICML.
- **Core idea**: Track per-parameter contribution Ω_i to
  loss reduction along the trajectory; regularise against
  changes weighted by Ω_i. No need for Fisher estimation.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

## 5. Surprise, Salience, and Affective Gating

### 5.1 Information-Theoretic Salience

- **Year / citation**: Bruce & Tsotsos 2005. "Saliency
  Based on Information Maximization". *NeurIPS 2005*.
- **Core idea**: Salience is the self-information of a
  local feature, S(x) = -log p(x), where p is a learned
  density model of the input.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 5.2 Affective Gating and the Amygdala

- **Year / citation**: LeDoux 1996 (*The Emotional Brain*);
  Phelps & LeDoux 2005. "Contributions of the Amygdala to
  Emotion Processing". *Neuron* 48(2): 175–187.
- **Core idea**: The amygdala tags high-salience events for
  preferential consolidation. Affective valence is
  represented as a scalar; arousal is the gate.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ⚠️ Mechanism; not an algorithm
  per se.

## 6. Cognitive Control / Executive Function

### 6.1 Hierarchical Reinforcement Learning (Options Framework)

- **Year / citation**: Sutton, Precup, Singh 1999. "Between
  MDPs and Semi-MDPs: A Framework for Temporal Abstraction
  in Reinforcement Learning". *AIJ* 112: 181–211.

- **Core idea**: An *option* is a closed-loop policy with
  an initiation set I and a termination condition β. The
  intra-option SMDP Q-learning converges to the optimal
  hierarchical policy.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 6.2 DYNA

- **Year / citation**: Sutton 1990. "Integrated Architectures
  for Learning, Planning, and Reacting Based on Approximating
  Dynamic Programming". *ICML 1990* (pp. 216–224).
- **Core idea**: Combine model-free RL with a learned model
  for planning. Each step: (1) act, (2) learn value function,
  (3) update model, (4) k simulated steps with the model to
  improve the value function.
- **Confirmation flag**: 🟢 `confirmed-curated`
- **Ready-for-promotion**: ✅ Yes.

### 6.3 Model-Based RL and MCTS

- **Year / citation**: Browne et al. 2012. "A Survey of
  Monte Carlo Tree Search Methods". *IEEE TCIAIG* 4(1):
  1–43. Silver et al. 2016, 2017, 2018 (AlphaGo/Zero/MuZero).
- **Core idea**: Build a search tree incrementally; select by
  UCB; expand; rollout; back-up. UCT (Kocsis & Szepesvári
  2006) is the standard.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 6.4 Soft Actor-Critic (SAC)

- **Year / citation**: Haarnoja, Zhou, Abbeel, Levine 2018.
  "Soft Actor-Critic: Off-Policy Maximum Entropy Deep
  Reinforcement Learning with a Stochastic Actor". ICML.
- **Core idea**: Maximum-entropy RL: J(π) = Σ_t E[r_t +
  α H(π(·|s_t))]. Off-policy actor-critic with a
  reparameterised squashed Gaussian.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 6.5 PPO (Proximal Policy Optimisation)

- **Year / citation**: Schulman, Wolski, Dhariwal, Radford,
  Klimov 2017. "Proximal Policy Optimization Algorithms".
  arXiv:1707.06347.
- **Core idea**: Clip the ratio r_t(θ) = π_θ(a_t|s_t) /
  π_θ_old(a_t|s_t) to [1-ε, 1+ε] in the surrogate objective.
  First-order only; very stable.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 6.6 Decision Transformer

- **Year / citation**: Chen et al. 2021. "Decision
  Transformer: Reinforcement Learning via Sequence
  Modeling". NeurIPS 2021.
- **Core idea**: Treat RL as conditional sequence modelling.
  Predict the next action given the past (return-to-go,
  state, action) tokens.
- **Confirmation flag**: 🟢 `confirmed-curated`
- **Ready-for-promotion**: ✅ Yes (state-of-the-art on
  long-horizon tasks).

## 7. Metacognition

### 7.1 Type-2 Signal Detection Theory

- **Year / citation**: Galvin, Podd, Drga, Whitmore 2003.
  "Type 2 Tasks in the Theory of Signal Detectability:
  Discrimination Between Correct and Incorrect Decisions".
  *Psychonomic Bulletin & Review* 10(4): 843–876.
- **Core idea**: For each stimulus-response pair, the
  observer reports a *confidence* rating. The Type-2 ROC
  curve (hit rate vs false-alarm rate as a function of
  confidence threshold) characterises metacognition. AUROC2
  is the standard metric.
- **Confirmation flag**: 🟢 `confirmed-curated`
- **Ready-for-promotion**: ✅ Yes.

### 7.2 Nelson-Narens Framework

- **Year / citation**: Nelson & Narens 1990. "Metamemory: A
  Theoretical Framework and New Findings". In Bower (ed.)
  *The Psychology of Learning and Motivation* vol. 26.
- **Core idea**: A *monitoring* loop (object-level → meta-
  level) reports judgments of learning, feeling-of-knowing,
  confidence; a *control* loop (meta-level → object-level)
  allocates study time, search effort, etc.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

## 8. Promotion Summary

| #  | Algorithm                       | Year | Operator name                  |
|----|---------------------------------|------|--------------------------------|
| 1  | ACT-R activation                | 1993 | `actr-activation`             |
| 2  | Soar decision cycle             | 1987 | `soar-decide`                 |
| 3  | Global Workspace (Baars)        | 1988 | `gwt-broadcast`               |
| 4  | Soft attention (Bahdanau)       | 2014 | `attention-soft`              |
| 5  | Multi-head self-attention       | 2017 | `attention-multihead`         |
| 6  | Squeeze-Excitation              | 2018 | `attention-se`                |
| 7  | Itti-Koch saliency              | 1998 | `saliency-itti`               |
| 8  | Kalman / EKF                    | 1960 | `ekf-step`                    |
| 9  | Particle filter                 | 1993 | `particle-filter-step`        |
| 10 | Bayesian surprise               | 2006 | `bayesian-surprise`           |
| 11 | Free-energy principle           | 2010 | `free-energy-step`            |
| 12 | Predictive coding               | 1999 | `predictive-coding-step`      |
| 13 | Baum-Welch (HMM)                | 1972 | `baum-welch`                  |
| 14 | Hebbian / Oja / STDP            | 1949 | `hebb-step` / `oja-step` / `stdp-step` |
| 15 | Backprop                        | 1986 | `backprop-step`               |
| 16 | Adam optimiser                  | 2014 | `adam-step`                   |
| 17 | EWC / SI (continual learning)   | 2017 | `ewc-regularise` / `si-regularise` |
| 18 | Options (HRL)                   | 1999 | `options-step`                |
| 19 | DYNA                            | 1990 | `dyna-plan`                   |
| 20 | MCTS / UCT                      | 2006 | `mcts-search`                 |
| 21 | PPO                             | 2017 | `ppo-step`                    |
| 22 | SAC                             | 2018 | `sac-step`                    |
| 23 | Decision Transformer            | 2021 | `decision-transformer-step`   |
| 24 | Type-2 SDT                      | 2003 | `metacog-roc2`                |

## 9. See also

- `sxl-operators.md` — symbolic cognitive algorithms.
- `neuro-primitives.md` — neuro-computational primitives.
- `memory-reasoning.md` — memory architectures, knowledge
  representation, RL, causal discovery.
- `README.md` — overview of the research knowledge base.
