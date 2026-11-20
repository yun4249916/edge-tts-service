# edge-tts-service
Edge TTS（微软 Edge 在线配音）做成一个小网页接口，部署在 Railway 上。
- GET / 健康检查
- GET /voices 列出中文音色
- GET /tts?text=你好&voice=zh-CN-XiaoxiaoNeural 返回 MP3
默认音色 zh-CN-XiaoxiaoNeural（晓晓）。
