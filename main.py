import asyncio
import websockets
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

async def handle_websocket(websocket, path):
    try:
        async for message in websocket:
            # 接收客户端发送的消息（这里假设客户端发送的消息就是文章内容）
            ARTICLE = message

            # 使用tokenizer编码文本数据
            input_ids = tokenizer(ARTICLE, return_tensors="pt").input_ids

            # 使用模型生成文本
            output = model.generate(input_ids, max_length=150)

            # 解码生成的文本
            decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)

            # 将生成的文本作为响应发送给客户端
            await websocket.send(decoded_output)

    except websockets.ConnectionClosed:
        pass

tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")

# 将函数封装在main()函数中，使得可异步循环调用
async def main():

    # 启动WebSocket服务器，监听在指定的主机和端口
    start_server = await websockets.serve(handle_websocket, "localhost", 8765)

    await start_server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())