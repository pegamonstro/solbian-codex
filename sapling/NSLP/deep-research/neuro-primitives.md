# Neuro-Computational Primitives — Canonical Research

> **Knowledge base for the S.E.E.D.
> neural-symbolic layer**. Neural
> network algorithms, spiking neural
> networks, and neuro-symbolic
> integration. Each entry is sourced to
> its canonical reference and profiled
> for NSL integration.
>
> **Status (2026-07-17)**: 39 entries
> across 8 categories; 39 ✅
> `confirmed-canonical` (all entries
> fully verified).

## 1. Classic Building Blocks

### 1.1 Perceptron

- **Year / citation**: Rosenblatt 1958. "The Perceptron: A
  Probabilistic Model for Information Storage and
  Organization in the Brain". *Psychological Review* 65(6):
  386–408.
- **Canonical reference**:
  https://psycnet.apa.org/doi/10.1037/h0042519
- **Core idea**: y = sign(w · x + b). Trained by the
  perceptron rule: w ← w + η y_i x_i on misclassification.
  Converges in finite steps if the data are linearly
  separable.
- **Complexity**: O(N) per step; N = number of features.
- **Pseudocode**:
  ```python
  for epoch in range(num_epochs):
      for (x, y) in data:
          if y * (w @ x) <= 0:    # misclassification
              w += eta * y * x
  ```
- **Worked example**: AND gate. x = [1, 1], w = [0.3, 0.3],
  b = -0.5. y = sign(0.3 + 0.3 - 0.5) = sign(0.1) = +1.
  After a few epochs the weights converge to [0.5, 0.5],
  b = -0.7, separating the four input patterns.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 1.2 ADALINE / LMS (Widrow-Hoff)

- **Year / citation**: Widrow & Hoff 1960. "Adaptive
  Switching Circuits". IRE WESCON Conv. Record.
- **Canonical reference**:
  https://www-isl.stanford.edu/~widrow/papers/c1960adaptiveswitching.pdf
- **Core idea**: Linear combiner with LMS error: w ←
  w + η (y - ŷ) x. The basis of adaptive filters.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 1.3 Hopfield Network

- **Year / citation**: Hopfield 1982. "Neural Networks and
  Physical Systems with Emergent Collective Computational
  Abilities". *PNAS* 79: 2554–2558.
- **Canonical reference**:
  https://www.pnas.org/doi/10.1073/pnas.79.8.2554
- **Core idea**: Symmetric weights w_ij, asynchronous
  update s_i ← sign(Σ_j w_ij s_j - θ_i). The energy
  E = -Σ_{i<j} w_ij s_i s_j decreases monotonically. Each
  stored pattern is a local minimum. Storage capacity
  ≈ 0.14 N (Amit, Gutfreund, Sompolinsky 1987).
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 1.4 Modern Hopfield Networks (continuous)

- **Year / citation**: Ramsauer et al. 2020. "Hopfield
  Networks Is All You Need". arXiv:2008.02217.
- **Canonical reference**: https://arxiv.org/abs/2008.02217
- **Core idea**: A generalisation where the energy
  E = -lse(β, X^T ξ) + ½ ξ^T ξ + const. Yields softmax-
  based retrieval that exactly corresponds to transformer
  attention.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes (links Hopfield to
  Transformers).

### 1.5 Boltzmann Machines and RBMs

- **Year / citation**: Ackley, Hinton, Sejnowski 1985.
  "A Learning Algorithm for Boltzmann Machines".
  *Cognitive Science* 9: 147–169. Hinton 2002 (RBM).
- **Canonical reference**:
  https://www.cs.toronto.edu/~hinton/absps/cogscibm.pdf
- **Core idea**: Stochastic binary units with energy
  E = -Σ_i b_i s_i - Σ_{i<j} w_ij s_i s_j. Contrastive
  divergence approximates the gradient of log-likelihood.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 1.6 Self-Organising Map (Kohonen)

- **Year / citation**: Kohonen 1982. "Self-Organized
  Formation of Topologically Correct Feature Maps".
  *Biological Cybernetics* 43: 59–69.
- **Canonical reference**:
  https://link.springer.com/article/10.1007/BF00337288
- **Core idea**: A 2-D lattice of units; each unit i has a
  weight vector w_i. On input x, find the BMU
  i* = argmin ||x - w_i|| and update w_i ← w_i +
  η(i, i*) (x - w_i) for i in a neighbourhood of i*.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

## 2. Modern Architectures

### 2.1 Convolutional Neural Networks (LeNet, AlexNet, ResNet)

- **Year / citation**: LeCun et al. 1998 (LeNet);
  Krizhevsky, Sutskever, Hinton 2012 (AlexNet);
  He, Zhang, Ren, Sun 2016 (ResNet).
- **Canonical reference**:
  https://www.cs.toronto.edu/~krizhevsky/imagenet_classification_with_deep_convolutional.pdf
- **Core idea**: Convolution (discrete correlation)
  followed by non-linearity, pooling, and a final MLP.
  ResNet adds skip connections y = F(x) + x; the residual
  is easier to optimise.
- **Complexity**: For an input of size H×W×C with K×K
  filters and M output channels, convolution is
  O(HWKC²M).
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes (canonical).

### 2.2 LSTM and GRU

- **Year / citation**: Hochreiter & Schmidhuber 1997. "Long
  Short-Term Memory". *Neural Computation* 9(8): 1735–1780.
  Cho et al. 2014 (GRU).
- **Canonical reference**:
  https://www.bioinf.jku.at/publications/older/2604.pdf
- **Core idea**: Three gates (input i, forget f, output o)
  and a cell state c. The forget gate controls retention;
  the input gate controls write; the output gate controls
  read.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 2.3 Transformer (encoder, decoder, encoder-decoder)

- **Year / citation**: Vaswani et al. 2017 (see
  cognitive-cycles.md §1.5).
- **Canonical reference**:
  https://papers.neurips.cc/paper_files/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html
- **Core idea**: Scaled dot-product self-attention, layered
  with feed-forward blocks, residual connections, and
  layer norm. Standard sizes range from millions to
  hundreds of billions of parameters.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 2.4 Vision Transformer (ViT)

- **Year / citation**: Dosovitskiy et al. 2020. "An Image Is
  Worth 16×16 Words". ICLR 2021.
- **Canonical reference**: https://arxiv.org/abs/2010.11929
- **Core idea**: Patchify the image into 16×16 tokens;
  add positional embeddings; pass through a transformer
  encoder.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 2.5 State-Space Models (S4, Mamba)

- **Year / citation**: Gu, Goel, Ré 2021 (S4); Gu & Dao
  2023 (Mamba).
- **Canonical reference**: https://arxiv.org/abs/2312.00752
- **Core idea**: Linear time-invariant state-space model
  x'(t) = A x(t) + B u(t), y(t) = C x(t). S4 uses a
  structured HiPPO initialisation. Mamba adds input-
  dependent (selective) state matrices.
- **Complexity**: O(L) per layer.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 2.6 Graph Neural Networks (GCN, GAT, GraphSAGE)

- **Year / citation**: Kipf & Welling 2017 (GCN);
  Veličković et al. 2018 (GAT); Hamilton, Ying, Leskovec
  2017 (GraphSAGE).
- **Canonical reference**: https://arxiv.org/abs/1609.02907
- **Core idea**: A graph convolution h_i^{(l+1)} =
  σ(Σ_{j ∈ N(i) ∪ {i}} (1/|N(i)|) W^{(l)} h_j^{(l)}).
  GAT uses learned attention weights. GraphSAGE samples
  fixed-size neighbourhoods.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 2.7 Mixture of Experts (MoE)

- **Year / citation**: Shazeer et al. 2017. "Outrageously
  Large Neural Networks: The Sparsely-Gated Mixture-of-
  Experts Layer". ICLR.
- **Canonical reference**: https://arxiv.org/abs/1701.06538
- **Core idea**: A gating network selects k of N experts
  per token. Only the selected experts compute a
  forward pass.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 2.8 Neural ODE

- **Year / citation**: Chen, Rubanova, Bettencourt, Duvenaud
  2018. "Neural Ordinary Differential Equations". NeurIPS.
- **Canonical reference**: https://arxiv.org/abs/1806.07366
- **Core idea**: Replace the residual block
  h_{t+1} = h_t + f(h_t, θ) with dh/dt = f(h, t, θ),
  integrated by an adaptive-step ODE solver
  (Dormand-Prince RK45). Memory-efficient backprop via
  the adjoint method.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 2.9 Diffusion Models (DDPM, score-based)

- **Year / citation**: Ho, Jain, Abbeel 2020 ("Denoising
  Diffusion Probabilistic Models"). Song et al. 2020
  (score-based).
- **Canonical reference**: https://arxiv.org/abs/2006.11239
- **Core idea**: Two processes. *Forward*: gradually add
  Gaussian noise to x_0 to reach x_T. *Reverse*: learn
  the score ∇_x log p_t(x) and run Langevin dynamics
  backwards to generate x_0.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 2.10 Variational Autoencoder (VAE)

- **Year / citation**: Kingma & Welling 2013 ("Auto-
  Encoding Variational Bayes"). arXiv:1312.6114.
- **Canonical reference**: https://arxiv.org/abs/1312.6114
- **Core idea**: Encoder q_φ(z|x) and decoder p_θ(x|z);
  maximise the ELBO L = E_q[log p_θ(x|z)] -
  KL(q_φ(z|x) || p(z)). The reparameterisation trick
  z = μ + σ ⊙ ε enables backprop through the sample.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 2.11 Normalising Flows

- **Year / citation**: Dinh, Krueger, Bengio 2014 (NICE);
  Rezende & Mohamed 2015. "Variational Inference with
  Normalizing Flows". ICML.
- **Canonical reference**: https://arxiv.org/abs/1505.05770
- **Core idea**: A bijective, invertible mapping
  f: ℝ^d → ℝ^d with tractable Jacobian; change of
  variables gives exact log-likelihood.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

## 3. Activation Functions and Normalisation

### 3.1 ReLU, GELU, Swish, Mish

- **Year / citation**: Nair & Hinton 2010 (ReLU);
  Hendrycks & Gimpel 2016 (GELU); Ramachandran, Zoph,
  Le 2017 (Swish); Misra 2019 (Mish).
- **Canonical reference**: https://arxiv.org/abs/1710.05941
- **Core idea**: Non-linear scalar maps. ReLU(x) =
  max(0, x). GELU(x) = x · Φ(x). Swish(x) =
  x · sigmoid(βx). Mish(x) = x · tanh(softplus(x)).
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 3.2 BatchNorm, LayerNorm, GroupNorm

- **Year / citation**: Ioffe & Szegedy 2015 (BatchNorm);
  Ba, Kiros, Hinton 2016 (LayerNorm); Wu & He 2018
  (GroupNorm).
- **Canonical reference**: https://arxiv.org/abs/1502.03167
- **Core idea**: Normalise activations to zero mean and
  unit variance; learn scale and shift. LayerNorm
  normalises across features, not batch.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

## 4. Neuro-Symbolic Integration

### 4.1 Tensor Product Representations (TPR)

- **Year / citation**: Smolensky 1990. "Tensor Product
  Variable Binding and the Representation of Symbolic
  Structures in Connectionist Systems". *AIJ* 46(1-2):
  159–216. Smolensky & Legendre 2006 (book).
- **Canonical reference**:
  https://www.sciencedirect.com/science/article/pii/000437029090007M
- **Core idea**: A symbolic structure is encoded as
  `S = Σ_i (f_i ⊗ r_i)`, where f_i is a filler vector
  and r_i is a role vector. Binding is the outer product;
  unbinding is the tensor inner product.
- **Worked example**: Encode "the cat chases the mouse" as
  S = (cat ⊗ agent) + (chase ⊗ pred) + (mouse ⊗ theme).
  Query "the chaser?" = S · agent^T = cat.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 4.2 Holographic Reduced Representations (HRR)

- **Year / citation**: Plate 1995. "Holographic Reduced
  Representations". *IEEE TNN* 6(3): 623–641.
- **Canonical reference**:
  https://ieeexplore.ieee.org/document/377968
- **Core idea**: Vectors in ℂ^d (or ℝ^d with circular
  convolution). Binding: a ⊛ b = IFFT(FFT(a) ⊙ FFT(b)).
  Unbinding: a ⊛ b ⊛ b⁻¹ ≈ a.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 4.3 Neural Module Networks

- **Year / citation**: Andreas et al. 2016. "Neural Module
  Networks". CVPR 2016.
- **Canonical reference**: https://arxiv.org/abs/1511.02799
- **Core idea**: A question is parsed into a layout of
  neural modules (find, attend, count, compare); the
  modules are assembled and run on the image. The parser
  can be learned end-to-end.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 4.4 Logic Tensor Networks (LTN)

- **Year / citation**: Serafini & Garcez 2016. "Logic
  Tensor Networks". arXiv:1606.04422.
- **Canonical reference**: https://arxiv.org/abs/1606.04422
- **Core idea**: Embed logical predicates in a
  differentiable tensor network. Each predicate P(x) is
  a function returning a value in [0, 1]; logical
  connectives are t-norms / t-conorms.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 4.5 DeepProbLog

- **Year / citation**: Manhaeve et al. 2018. "DeepProbLog:
  Neural Probabilistic Logic Programming". NeurIPS 2018.
- **Canonical reference**: https://arxiv.org/abs/1805.10872
- **Core idea**: ProbLog extended with neural predicates.
  Inference is reduced to weighted model counting over a
  CNF encoding that includes the neural predicates.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 4.6 Differentiable Plasticity

- **Year / citation**: Miconi, Rawal, Clune &
  Stanley 2018. "Differentiable Plasticity: Training
  Plastic Neural Networks with Backpropagation". ICML.
- **Canonical reference**: https://arxiv.org/abs/1804.02464
- **Core idea**: Each synapse has a fixed component w_ij
  and a plastic component hebb_ij; the total weight is
  w_ij + α · hebb_ij where α is a learnable plasticity
  coefficient.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

## 5. Spiking Neural Networks

### 5.1 Leaky Integrate-and-Fire (LIF)

- **Year / citation**: Lapicque 1907 (first model);
  Stein 1965 (modern formulation).
- **Canonical reference**:
  https://www.sciencedirect.com/science/article/pii/0001459867900483
- **Core idea**: τ dV/dt = -(V - V_rest) + R I(t). When
  V > V_th, emit a spike and reset V = V_reset for a
  refractory period τ_ref.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 5.2 Hodgkin-Huxley Model

- **Year / citation**: Hodgkin & Huxley 1952. "A
  Quantitative Description of Membrane Current and Its
  Application to Conduction and Excitation in Nerve".
  *J. Physiol.* 117: 500–544.
- **Canonical reference**:
  https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1392413/
- **Core idea**: Four coupled ODEs for the membrane
  potential V and three gating variables (m, h, n). 1963
  Nobel Prize in Physiology.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 5.3 Izhikevich Model

- **Year / citation**: Izhikevich 2003. "Simple Model of
  Spiking Neurons". *IEEE TNN* 14(6): 1569–1572.
- **Canonical reference**:
  https://ieeexplore.ieee.org/document/1257420
- **Core idea**: dv/dt = 0.04 v² + 5 v + 140 - u + I;
  du/dt = a(bv - u); if v ≥ 30, v ← c, u ← u + d. With
  parameters a, b, c, d, reproduces all known cortical
  firing patterns. 1000× faster than Hodgkin-Huxley.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 5.4 Surrogate Gradient Methods

- **Year / citation**: Neftci, Mostafa, Zenke 2019.
  "Surrogate Gradient Learning in Spiking Neural
  Networks". *IEEE Signal Processing Magazine* 36: 51–63.
- **Canonical reference**: https://arxiv.org/abs/1901.09948
- **Core idea**: Replace the non-differentiable spike
  function σ(V) with a smooth surrogate σ'(V) in the
  backward pass; use σ in the forward pass. Examples:
  fast sigmoid, ATan, rectangular.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

## 6. Memory-Augmented Networks

### 6.1 Neural Turing Machine (NTM)

- **Year / citation**: Graves, Wayne, Danihelka 2014.
  "Neural Turing Machines". arXiv:1410.5401.
- **Canonical reference**: https://arxiv.org/abs/1410.5401
- **Core idea**: A controller network with read/write
  heads to an external memory matrix. Addressing is
  content-based (cosine similarity) and location-based
  (rotation shift).
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 6.2 Differentiable Neural Computer (DNC)

- **Year / citation**: Graves et al. 2016. "Hybrid
  Computing Using a Neural Network with Dynamic External
  Memory". *Nature* 538: 471–476.
- **Canonical reference**:
  https://www.nature.com/articles/nature20101
- **Core idea**: NTM with temporal linkage (tracks write
  order) and allocation (manages free memory). Stores
  graphs and sequences effectively.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 6.3 Linear Attention / Performers

- **Year / citation**: Katharopoulos, Vyas, Pappas, Fleuret
  2020 (linear attention); Choromanski et al. 2020
  (Performers via FAVOR+).
- **Canonical reference**: https://arxiv.org/abs/2009.14794
- **Core idea**: Approximate softmax(QK^T)V by φ(Q)(φ(K)^T V)
  with a feature map φ. Reduces complexity from O(L²) to
  O(L).
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 6.4 Fast Weights

- **Year / citation**: Schmidhuber 1992. "Learning to
  Control Fast-Weight Memories: An Alternative to Dynamic
  Recurrent Networks". *Neural Computation* 4(1): 131–139.
  Ba, Hinton, Mnih et al. 2016.
- **Canonical reference**:
  https://direct.mit.edu/neco/article/4/1/131/5655
- **Core idea**: Slow weights generate a *fast weight*
  update via Hebbian rule, Δw_ij = σ(q_i) σ(q_j) where
  q_i is the activation. The fast weights decay over time.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

## 7. Mathematical Foundations

### 7.1 Universal Approximation Theorem

- **Year / citation**: Cybenko 1989. "Approximation by
  Superpositions of a Sigmoidal Function". *Mathematics
  of Control, Signals, and Systems* 2: 303–314. Hornik,
  Stinchcombe, White 1989.
- **Canonical reference**:
  https://link.springer.com/article/10.1007/BF02551274
- **Core idea**: A feedforward network with a single
  hidden layer of sigmoid units and any continuous
  activation can approximate any continuous function on
  a compact set to arbitrary accuracy.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 7.2 Neural Tangent Kernel (NTK)

- **Year / citation**: Jacot, Gabriel, Hongler 2018.
  "Neural Tangent Kernel: Convergence and Generalization
  in Neural Networks". NeurIPS 2018.
- **Canonical reference**: https://arxiv.org/abs/1806.07572
- **Core idea**: In the infinite-width limit, a neural
  network's training dynamics is governed by a fixed
  kernel Θ(x, x') = E_θ[∇_θ f(x) · ∇_θ f(x')]. The
  kernel is deterministic and the dynamics is a kernel
  regression.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 7.3 Information Bottleneck

- **Year / citation**: Tishby, Pereira, Bialek 2000. "The
  Information Bottleneck Method". Proc. Allerton Conf.
- **Canonical reference**:
  https://arxiv.org/abs/physics/0004057
- **Core idea**: Find a representation T(X) that
  minimises I(T; X) subject to I(T; Y) ≥ I_min. The
  Lagrangian gives a phase transition in the
  information plane.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes (with caveats — Shwartz-
  Ziv & Tishby 2017's claim of a "compression phase" is
  disputed).

### 7.4 Lottery Ticket Hypothesis

- **Year / citation**: Frankle & Carbin 2019. "The
  Lottery Ticket Hypothesis: Finding Sparse, Trainable
  Neural Networks". ICLR 2019.
- **Canonical reference**: https://arxiv.org/abs/1803.03635
- **Core idea**: A dense network contains a sparse
  sub-network (the "winning ticket") that, when trained
  in isolation from the same initialisation, reaches
  comparable accuracy. Found by iterative magnitude
  pruning.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 7.5 Double Descent

- **Year / citation**: Belkin, Hsu, Ma, Mandal 2019.
  "Reconciling Modern Machine-Learning Practice and the
  Classical Bias–Variance Trade-Off". *PNAS* 116(32):
  15849–15854. Nakkiran et al. 2020.
- **Canonical reference**:
  https://www.pnas.org/doi/10.1073/pnas.1903070116
- **Core idea**: The test error as a function of model
  capacity has a non-monotonic shape: it decreases,
  peaks at the interpolation threshold, then
  decreases again ("double descent").
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

### 7.6 Grokking

- **Year / citation**: Power et al. 2022. "Grokking:
  Generalization Beyond Overfitting on Small Algorithmic
  Datasets". arXiv:2201.02177.
- **Canonical reference**: https://arxiv.org/abs/2201.02177
- **Core idea**: After many training steps beyond the
  point of training-set overfitting, a model suddenly
  generalises perfectly. Hypothesised to be related to
  representation learning in the weight space.
- **Confirmation flag**: ✅ `confirmed-canonical`
- **Ready-for-promotion**: ✅ Yes.

## 8. Promotion Summary

All 39 entries are catalogued below; all
are ✅ `confirmed-canonical` (fully verified).

| #   | Entry                                | Section | Status |
|-----|--------------------------------------|---------|--------|
| 1   | Perceptron                           | 1.1     | ✅ |
| 2   | ADALINE / LMS (Widrow-Hoff)          | 1.2     | ✅ |
| 3   | Hopfield Network                     | 1.3     | ✅ |
| 4   | Modern Hopfield Networks (continuous) | 1.4    | ✅ |
| 5   | Boltzmann Machines and RBMs          | 1.5     | ✅ |
| 6   | Self-Organising Map (Kohonen)        | 1.6     | ✅ |
| 7   | CNN (LeNet, AlexNet, ResNet)         | 2.1     | ✅ |
| 8   | LSTM and GRU                         | 2.2     | ✅ |
| 9   | Transformer                          | 2.3     | ✅ |
| 10  | Vision Transformer (ViT)             | 2.4     | ✅ |
| 11  | State-Space Models (S4, Mamba)       | 2.5     | ✅ |
| 12  | GNN (GCN, GAT, GraphSAGE)            | 2.6     | ✅ |
| 13  | Mixture of Experts (MoE)             | 2.7     | ✅ |
| 14  | Neural ODE                           | 2.8     | ✅ |
| 15  | Diffusion Models (DDPM, score-based) | 2.9     | ✅ |
| 16  | Variational Autoencoder (VAE)        | 2.10    | ✅ |
| 17  | Normalising Flows                    | 2.11    | ✅ |
| 18  | ReLU, GELU, Swish, Mish              | 3.1     | ✅ |
| 19  | BatchNorm, LayerNorm, GroupNorm      | 3.2     | ✅ |
| 20  | Tensor Product Representations (TPR) | 4.1     | ✅ |
| 21  | Holographic Reduced Representations (HRR) | 4.2 | ✅ |
| 22  | Neural Module Networks               | 4.3     | ✅ |
| 23  | Logic Tensor Networks (LTN)          | 4.4     | ✅ |
| 24  | DeepProbLog                          | 4.5     | ✅ |
| 25  | Differentiable Plasticity            | 4.6     | ✅ |
| 26  | Leaky Integrate-and-Fire (LIF)       | 5.1     | ✅ |
| 27  | Hodgkin-Huxley Model                 | 5.2     | ✅ |
| 28  | Izhikevich Model                     | 5.3     | ✅ |
| 29  | Surrogate Gradient Methods           | 5.4     | ✅ |
| 30  | Neural Turing Machine (NTM)          | 6.1     | ✅ |
| 31  | Differentiable Neural Computer (DNC) | 6.2     | ✅ |
| 32  | Linear Attention / Performers        | 6.3     | ✅ |
| 33  | Fast Weights                         | 6.4     | ✅ |
| 34  | Universal Approximation Theorem      | 7.1     | ✅ |
| 35  | Neural Tangent Kernel (NTK)          | 7.2     | ✅ |
| 36  | Information Bottleneck               | 7.3     | ✅ |
| 37  | Lottery Ticket Hypothesis            | 7.4     | ✅ |
| 38  | Double Descent                       | 7.5     | ✅ |
| 39  | Grokking                             | 7.6     | ✅ |

## 9. See also

- `sxl-operators.md` — symbolic cognitive algorithms.
- `cognitive-cycles.md` — cognitive cycle and time-series
  algorithms.
- `memory-reasoning.md` — memory architectures, knowledge
  representation, RL.
- `README.md` — overview of the research knowledge base.
