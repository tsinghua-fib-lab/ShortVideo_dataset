from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess
import os
from tqdm import tqdm
model_dir = "./sensevoicesmall"

model = AutoModel(
    model=model_dir,
    vad_model="fsmn-vad",
    vad_kwargs={"max_single_segment_time": 30000},
    device="cuda:0",
)

for i in tqdm(range(1,len(os.listdir('./audio'))+1)):
    # en
    try:
        res = model.generate(
            input=f"./audio/"+str(i)+".mp3",
            cache={},
            language="zn",  # "zn", "en", "yue", "ja", "ko", "nospeech"
            use_itn=True,
            batch_size_s=60,
            merge_vad=True,  #
            merge_length_s=15,
        )
        text = rich_transcription_postprocess(res[0]["text"])
        with open('./asr_zn/'+str(i)+'.txt', 'w') as file:
                file.write(text)
    except:
        with open('./asr_zn/'+str(i)+'.txt', 'w') as file:
            print('error in '+str(i)+'.mp3')
            file.write('')
    # print(text)