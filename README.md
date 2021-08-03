
![rad_flowchart](https://user-images.githubusercontent.com/84754885/120110941-6b938b80-c178-11eb-9929-c5a95e5ac868.png)

# RAD Measure

This repository implements tools for general purpose RAD calculation. In particular, it contains specific VQA tools that integrate with our proposed dataset.

Please see our paper for more details: [Are VQA systems RAD? Measuring robustness to augmented data with focused interventions](https://arxiv.org/abs/2106.04484).

## Installation
```sh
pip install -U rad-measure
```

## Our YesNoVQA Dataset

Please visit our website for [downloads, examples, and usage instructions](https://danrosenberg.github.io/rad-measure/).

To download our dataset:
```python
import rad_measure.vqa_utils as rad_vqa

questions, annotations = rad_vqa.get_questions_and_annotations(download=True)
```

### Code

Additional tools coming soon...
