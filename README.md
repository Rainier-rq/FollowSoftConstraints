# Step-by-Step Mastery: Enhancing Soft Constraint Following Ability of Large Language Models
[![Github](https://img.shields.io/static/v1?logo=github&style=flat&color=pink&label=github&message=Rainier-rq/FollowSoftConstraints)]([https://github.com/YJiangcm/FollowBench](https://github.com/meowpass/FollowComplexInstruction))


Official implementation of the paper "Step-by-Step Mastery: Enhancing Soft Constraint Following Ability of Large Language Models". 

We systematically study **how to enhance the ability of LLMs to follow soft constraints**, addressing the following research questions:
- ***How to construct* multi-constraint instruction following dataset**
  - To enable the model to learn how to follow each constraint, we increase only one constraint at a time, enabling the model progressively learn to follow each constraint during the training process.
- ***How to obtain* high-quality outputs?**
  - We introduce Judger to reorder the outputs based on the extent of constraint following to ensure the quality of outputs.
- ***How to effectively utilize* the data obtained through Judger reording?**
  - We we develop a training paradigm based on curriculum learning to enhance the training process.
  - We conduct extensive experiments to prove the effectiveness of our methods in terms of *overall performance and generalization abilities*.



![image](https://github.com/happy12348/FollowSoftConstraints/blob/master/method.jpg)

## 🔥Updates
* 2025/1/8: We posted our [paper](https://arxiv.org/pdf/2404.15846).
* 2025/1/7:  We released the data and code of FollowSoftConstraints.

## ⚙️How to Use the Code

### Install Dependencies

```
conda create -n fsc python=3.10.9
conda activate fsc
conda install pytorch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1 pytorch-cuda=11.7 -c pytorch -c nvidia
pip install -r requirements.txt
```

### Obtain Datasets with High-Quality Outputs
To obtain datasets with high-quality outputs: 
- First, we progressively construct the dataset. 
- Then, we introduce Judger to reorder the outputs to ensure the quality of outputs.
Here, you can complete the whole procedure by running the script `gen_data.sh`:

```shell
python ../get_data/gen_data.py \
    --seed_path=../get_data/data/seed_data.jsonl  \
    --dpo_data_path=../get_data/data/dpo.jsonl \
    --ift_data_path=../get_data/data/ift.jsonl \
    --api_key=YOUR_API_KEY_TO_ACESS_GPT4 \
```

### Curriculum-based Training Paradigm
We adopt Direct Preference Optimization (DPO) to leverage both the positive and negative samples from the Judger reording process. Moreover, we develop a training paradigm based on curriculum learning to enhance the training process.

Here, you can complete the whole procedure by running the following script:

```shell
cd CL_train
```
In the first stage, the model is trained using the the datasets corresponding to simpler curriculums. 
```shell
llamafactory-cli train lora_dpo_easy.yaml
```
Then the trained model is further trained using the datasets corresponding to the more challenging curriculums.
```shell
llamafactory-cli train lora_dpo_hard.yaml
```
## Citation
```
@misc{he2024complex,
      title={From Complex to Simple: Enhancing Multi-Constraint Complex Instruction Following Ability of Large Language Models}, 
      author={Qianyu He and Jie Zeng and Qianxi He and Jiaqing Liang and Yanghua Xiao},
      year={2024},
      eprint={2404.15846},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```
