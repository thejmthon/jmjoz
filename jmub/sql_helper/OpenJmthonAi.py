from sqlalchemy import Column, Integer, String

from ..core.logger import logging
from . import BASE, SESSION

LOGS = logging.getLogger(__name__)


class OpenJmthonAi(BASE):
    __tablename__ = "openai_config"
    model_id = Column(Integer, primary_key=True)
    model = Column(String(255))
    temperature = Column(String(255))
    max_tokens = Column(String(255))
    top_p = Column(String(255))
    frequency_penalty = Column(String(255))
    presence_penalty = Column(String(255))
    text_before_prompt = Column(String(2048))
    text_after_prompt = Column(String(255))

    def __init__(
        self,
        model_id,
        model="text-davinci-003",
        temperature="0.7",
        max_tokens="2048",
        top_p="1",
        frequency_penalty="0",
        presence_penalty="0",
        text_before_prompt="",
        text_after_prompt="",
    ):
        self.model_id = 1
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.text_before_prompt = text_before_prompt
        self.text_after_prompt = text_after_prompt

    def __repr__(self):
        return (
            "<OpenJmthonAi(model_id=%d, model='%s', temperature='%s', max_tokens='%s', top_p='%s', frequency_penalty='%s', presence_penalty='%s', text_before_prompt='%s', text_after_prompt='%s')>"
            % (
                int(self.model_id),
                self.model,
                self.temperature,
                self.max_tokens,
                self.top_p,
                self.frequency_penalty,
                self.presence_penalty,
                self.text_before_prompt,
                self.text_after_prompt,
            )
        )


OpenJmthonAi.__table__.create(checkfirst=True)


def setOpenJmthonAi(
    model_name,
    temp,
    maxtoken,
    topp,
    frequencypenalty,
    presencepenalty,
    textbeforeprompt,
    textafterprompt,
):
    data = SESSION.query(OpenJmthonAi).filter(OpenJmthonAi.model_id == 1).first()
    LOGS.info(f"\nLog: setOpenJmthonAi: data={data}\n")
    if (not data) or (data is None):
        LOGS.info(f"\nLog: setOpenJmthonAi: data found none!! Adding...\n")
        data = OpenJmthonAi(
            model_id=1,
            model=model_name,
            temperature=temp,
            max_tokens=maxtoken,
            top_p=topp,
            frequency_penalty=frequencypenalty,
            presence_penalty=presencepenalty,
            text_before_prompt=textbeforeprompt,
            text_after_prompt=textafterprompt,
        )
    else:
        LOGS.info("\nLog: setOpenJmthonAi: data exists already!! Updating...\n")
        data.model = model_name
        data.temperature = temp
        data.max_tokens = maxtoken
        data.top_p = topp
        data.frequency_penalty = frequencypenalty
        data.presence_penalty = presencepenalty
        data.text_before_prompt = textbeforeprompt
        data.text_after_prompt = textafterprompt
    try:
        SESSION.add(data)
        SESSION.commit()
        LOGS.info("\nLog: setOpenJmthonAi: data commited!!\n")
        LOGS.info(f"\nLog: setOpenJmthonAi: data={data}\n")
        return True
    except Exception as e:
        LOGS.info(f"\nLog: setOpenJmthonAi: Error:\n\n\n{str(e)}\n")
        return False


def getOpenJmthonAi():
    data = SESSION.query(OpenJmthonAi).filter(OpenJmthonAi.model_id == 1).first()
    if (not data) or data is None:
        data = OpenJmthonAi(
            model_id=1,
            model="text-davinci-003",
            temperature="0.7",
            max_tokens="2048",
            top_p="1",
            frequency_penalty="0",
            presence_penalty="0",
            text_before_prompt="",
            text_after_prompt="",
        )
        try:
            SESSION.add(data)
            SESSION.commit()
        except:
            return None
    res_list = [
        str(data.model),
        float(data.temperature),
        int(data.max_tokens),
        float(data.top_p),
        float(data.frequency_penalty),
        float(data.presence_penalty),
        str(data.text_before_prompt),
        str(data.text_after_prompt),
    ]
    SESSION.close()
    return res_list
