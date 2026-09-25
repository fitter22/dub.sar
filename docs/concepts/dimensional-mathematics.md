# Dimensional Mathematics

In DUB.SAR, quantities are not naked numbers. Every metrological measurement carries a dimensional unit that reflects physical reality and scribal measurement conventions.

---

## Metrological Dimensionality

Mesopotamian mathematical tablets measured real-world quantities: canal lengths, grain storage volumes, brick counts, and day labor. Mixing incompatible dimensions (such as adding length to area) was mathematically meaningless.

DUB.SAR enforces dimensional soundness at parse and compile time:

1. **Dimensional Homogeneity**: Addition and subtraction require quantities to share the identical physical dimension:
   $$\text{length} + \text{length} \to \text{length}$$
   $$\text{area} - \text{area} \to \text{area}$$
2. **Multiplicative Composition**: Multiplication and division compose dimensions:
   $$\text{length} \times \text{length} \to \text{area}$$
   $$\text{area} \times \text{length} \to \text{volume}$$
   $$\text{volume} / \text{time} \to \text{flow\_rate}$$
3. **Automatic Coherent Conversion**: When adding compatible units within the same dimension (such as `meter` and `centimeter`, or `kush3` and `nindan`), DUB.SAR automatically scales values to canonical base units using exact rational conversion factors.
4. **Compile-Time Safety**: Attempting to add quantities of mismatched dimensions (such as `length` and `mass`) produces a static diagnostic error before execution.
