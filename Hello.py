# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
import telegram
import asyncio
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, MessageHandler
import time
from datetime import datetime

LOGGER = get_logger(__name__)
CHAT_ID = '5506745859'
TELE_TOKEN = '6438318825:AAE9HGapmTQ853woseydqfunNnMak0RRNs0'
NOW_TIME = datetime.now().time()

def run():
    st.set_page_config(
        page_title="전국문화축제",
        page_icon="👋",
    )

    st.write("# 전국문화축제 조회")
  

    st.markdown(
        """
        데이터 제공 : 한국관광공사, 지방자치단체(공공데이터)
    """
    )
     
    st.image('img/fest_img.jpg')

async def msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 이미지 경로
    image_path = "img/fest_img.jpg"
    # 이미지 파일을 읽어 들여 채팅방으로 전송
    with open(image_path, "rb") as image_file:
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_file, caption="서버에서 보낸 이미지 파일입니다.")


if __name__ == "__main__":
    run()
     # 챗봇 application 인스턴스 생성
    application = ApplicationBuilder().token(TELE_TOKEN).build()
    # 핸들러 생성
    msg_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), msg)
    # 핸들러 추가
    application.add_handler(msg_handler)
    # 폴링 방식으로 실행
    application.run_polling()
