---
layout: cayman
classes: wide
---

# Download our Proposed Dataset

We have created three template-based augmentations for VQA datasets. Our dataset contains yes/no questions that were generated from questions about colors, counting, and object identification. For more information please see Section 2.2 in the [paper](https://arxiv.org/abs/2106.04484).

Load our dataset in the [VQA format](https://visualqa.org/download.html):

```python
import rad_measure.vqa_utils as rad_vqa

all_yn_questions, all_yn_annotations = rad_vqa.get_questions_and_annotations(download=True)
```

Load individual augmentation types:

```python
import rad_measure.vqa_utils as rad_vqa

val_ync_questions, val_ync_annotations = rad_vqa.get_questions_and_annotations(
    aug_type='colors', split='val')

all_ync_ynhm_questions, all_ync_ynhm_annotations = rad_vqa.get_questions_and_annotations(
    aug_type=['colors', 'how-many'], split='all')
```

# Evaluate Robustness with RAD

RAD calculation involves the simple workflow below. For more information please see Section 2.1 in the paper.

![RAD Flowchart](/assets/images/rad_flowchart.svg)

In code (coming soon):

```python
from rad_measure import rad

# Augment data
orig_data, y_orig_true = get_data()
aug_data, y_aug_true = augment_data(orig_data, y_orig_true)

# Extract predictions
y_orig_pred = model.predict(orig_data)
y_aug_pred = model.predict(aug_data)

# Evaluate robustness
rad(y_orig_true, y_orig_pred, y_aug_true, y_aug_pred)
```
