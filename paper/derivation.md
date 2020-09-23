# Unary Labeling CNF

## Notation

$y_i$ is a vector representing the unary label of node $i$.

$x_{ij}$ is a boolean representing the existence of an edge from node $i$ to $j$.

We use $\iff$ to denote logical equivalence, and $\rightarrow$ and $\leftrightarrow$ to denote the conditional (implies) and the biconditional, respectively. 

## Intro

The acyclicity check given by the paper is defined as:

$$
\begin{gathered}
\bigwedge(x_{ij} \rightarrow \text{less}(y_i, y_j)) \land \bigvee (\text{unary}(y_i)) \\
\iff \bigwedge(x_{ij} \rightarrow \exists u\ \text{lessunr}(y_i, y_j, u)) \land \bigvee (\text{unary}(y_i))
\end{gathered}
$$

We can split circuit up at the conjunction (and) and convert each part to CNF. The conjunction of two CNFs is a CNF.

## 1. Converting the *lessunr* circuit

Let's first convert the lessunr circuit:

$$
\bigwedge(x_{ij} \rightarrow \exists u\ \text{lessunr}(y_i, y_j, u))
$$

We remove the existential by *existential instantiation*, replacing each existential with a new constant symbol. 

Let $U_{ij}$ be a vector of new auxiliary variables associated with $y_i$ and $y_j$:

$$
\bigwedge(x_{ij} \rightarrow \text{lessunr}(y_i, y_j, U_{ij})) 
$$

Replace the implies with the equivalent clause, then 

$$
\begin{aligned}
&\bigwedge_{i,j \in [n]}(\neg x_{ij} \lor \text{lessunr}(y_i, y_j, U_{ij})) \\
\iff &\bigwedge_{i,j \in [n]}\bigg(\neg x_{ij} \lor \Big(\bigwedge_{k=1}^{n-1} \big((\neg y_{ik} \lor \neg U_{ijk}) \land (y_{jk} \lor \neg U_{ijk})\big) \land \bigvee_{k=1}^{n-1} (U_{ijk})\Big)\bigg)
\end{aligned}
$$

Distribute $\neg x_{ij}$ disjunction (or) over conjunction (and), twice:

$$
\begin{gathered}
\bigwedge_{i,j \in [n]}\bigg(\neg x_{ij} \textcolor{red}{\lor} \Big(\textcolor{red}{\bigwedge_{k=1}^{n-1}} \big((\neg y_{ik} \lor \neg U_{ijk}) \land (y_{jk} \lor \neg U_{ijk})\big) \land \bigvee_{k=1}^{n-1} (U_{ijk})\Big)\bigg)
\\
\iff \bigwedge_{i,j \in [n]}\Big(\bigwedge_{k=1}^{n-1} \big(\neg x_{ij} \textcolor{red}\lor ((\neg y_{ik} \lor \neg U_{ijk}) \textcolor{red}\land (y_{jk} \lor \neg U_{ijk}))\big) \land \bigvee_{k=1}^{n-1} (U_{ijk})\Big) \\
\iff \bigwedge_{i,j \in [n]}\Big(\bigwedge_{k=1}^{n-1} \big((\neg x_{ij} \lor \neg y_{ik} \lor \neg U_{ijk}) \land (\neg x_{ij} \lor y_{jk} \lor \neg U_{ijk})\big) \land \bigvee_{k=1}^{n-1} (U_{ijk})\Big)
\end{gathered}
$$

Finally, rearrange the conjunctions (and) to make the CNF more clear:

$$
\bigwedge_{i,j \in [n]}\Big(\bigwedge_{k=1}^{n-1} \big((\neg x_{ij} \lor \neg y_{ik} \lor \neg U_{ijk}) \land (\neg x_{ij} \lor y_{jk} \lor \neg U_{ijk})\big)\Big) \land \bigwedge_{i,j \in [n]}\big(\bigvee_{k=1}^{n-1} (U_{ijk}) \big)
$$

## 2. Converting the *unary* circuit

Now we convert the unary circut:

$$
\begin{gathered}
\bigwedge_{i\in[n]} \text{unary}(y_i) \\
\iff \bigwedge_{i\in[n]} (\bigwedge_{j=2}^{n-1} y_{i,j-1} \rightarrow y_{ij}) \\
\iff \bigwedge_{i\in[n]} (\bigwedge_{j=2}^{n-1} \neg y_{i,j-1} \lor y_{ij})
\end{gathered}
$$

And we're done!

The final CNF is given by: $\text{lessunrCNF} \land \text{unaryCNF}$
