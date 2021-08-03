import os
from pathlib import Path
import json

from typing import Union, List, Tuple

from .utils import download_url, extract_zip


def download_yes_no_vqa_data(dataroot: str = 'data/', overwrite: bool = False):
    """Download and extract our dataset to `<dataroot>/yes-no_vqa/`."""
    url = 'https://rad-measure.s3.eu-central-1.amazonaws.com/yes-no_vqa.zip'
    zip_path = os.path.join(dataroot, Path(url).name)

    # Skip if exists
    if os.path.exists(extract_zip(zip_path, ret_extracted_path=True)) and not overwrite:
        return

    # Download and extract
    download_url(url, zip_path)
    extract_zip(zip_path)


def get_questions_and_annotations(aug_types: Union[str, List[str]] = None, split: str = 'val',
                                  download: bool = False) -> Tuple[dict, dict]:
    """Get questions and annotation of the YesNoVQA dataset in the VQA format.

    This function assumes that the data was downloaded with:
        >>> download_yes_no_vqa_data(dataroot='data/')

    Arguments:
        aug_types: Get specific augmentations types. If None (default), get all types.
            Possible types are ['colors', 'how-many', 'what-kind'].
        split: VQAv2 split that the augmentations were generated from. May be one of
            ['train', 'val', 'all']. If 'all', concatenate and return both
            'train' and 'val' sets.
        download: If True, download the the YesNoVQA dataset to the default
            location, see :func:`download_yes_no_vqa_data`. If the data exists
            or `download == False`, do nothing.

    Returns:
        A tuple `(questions, annotations)`.
    """
    # Parse `types`
    all_types = ['colors', 'how-many', 'what-kind']
    if aug_types is None:
        aug_types = all_types
    elif isinstance(aug_types, str):
        aug_types = [aug_types]
    elif isinstance(aug_types, list):
        assert len(aug_types) <= 3
        assert all(isinstance(t, str) for t in aug_types)
        assert all(t in all_types for t in aug_types), f"Make sure that all the values in " \
                                                       f"`aug_types = '{aug_types}'` are in '{all_types}'."
    else:
        raise ValueError("`types` should be either a list or a string.")

    # Parse `split`
    assert split in ['train', 'val', 'all']
    if split == 'all':
        split = ['train', 'val']
    else:
        split = [split]

    # Download to the default location
    if download:
        download_yes_no_vqa_data()

    return _get_questions(aug_types, split), _get_annotations(aug_types, split)


def _get_data_path(aug_type, split, get_questions):
    ques_or_annot_str = 'questions' if get_questions else 'annotations'
    return f'data/yes-no_vqa/yes-no_from_{aug_type}_{split}_{ques_or_annot_str}.json'


def _get_questions(aug_types: List[str], splits: List[str]) -> dict:
    aug_datas = {'questions': []}
    for aug_type in aug_types:
        for split in splits:
            with open(_get_data_path(aug_type, split, get_questions=True), 'r') as f:
                aug_data = json.load(f)
            aug_datas['questions'].extend(aug_data['questions'])
    return aug_datas


def _get_annotations(aug_types: List[str], splits: List[str]) -> dict:
    aug_datas = {'annotations': []}
    for aug_type in aug_types:
        for split in splits:
            with open(_get_data_path(aug_type, split, get_questions=False), 'r') as f:
                aug_data = json.load(f)
            aug_datas['annotations'].extend(aug_data['annotations'])
    return aug_datas


def _test_loading():
    print("Dataset lengths:")
    for split in ['train', 'val', 'all']:
        for aug_type in ['colors', 'how-many', 'what-kind']:
            yes_no_vqa_questions, yes_no_vqa_annotations = get_questions_and_annotations(
                aug_types=aug_type, split=split, download=True)
            if split == 'all':
                continue
            data_str = f"{aug_type}_{split}"
            print(f"{data_str:>20}", len(yes_no_vqa_questions['questions']))
