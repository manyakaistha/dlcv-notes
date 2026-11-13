# Few-shot learning

Few-shot learning studies adaptation to a target task from a small labelled support set. In an $N$-way $K$-shot episode, there are $N$ classes and $K$ labelled support examples per class; a separate query set measures generalization. A feature encoder may be pretrained on many source examples before this episode. Prototypical networks average support embeddings for each class and classify a query according to distance from those prototypes. Other approaches fit a linear classifier or fine-tune model parameters. Episodic meta-learning is one way to train for such adaptation, but is not required by the definition. Zero-shot learning instead uses no labelled target-class examples, although class descriptions or other side information can be available.

## Why it matters here

Counting target support examples, rather than the size of the source training set, identifies the shot count in the exam.

**Appears in:** [[week-11-report]] · [[week-11-exam-notes]] · [[week-11-questions]]

## Related

[[contrastive-learning]] · [[clip-alignment]]
