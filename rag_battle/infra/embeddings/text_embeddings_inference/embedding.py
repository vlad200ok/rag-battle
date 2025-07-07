import numpy as np
import grpc
from rag_battle.infra.embeddings.text_embeddings_inference import tei_pb2, tei_pb2_grpc


async def embeddings_grpc(texts: list[str], host: str, port: int) -> np.ndarray:
    if not texts:
        return np.array([])
    # TODO: find out a reason of the behaviour
    #  async with grpc.aio.insecure_channel(f"{host}:{port}") as channel:
    #  It is stuck under load - sync code in async => the app is dead!
    channel = grpc.aio.insecure_channel(f"{host}:{port}")
    stub = tei_pb2_grpc.EmbedStub(channel)

    async def batch(texts_: list[str]):
        for text in texts_:
            # gRPC fails to embed empty string
            if not text:
                text = " "
            yield tei_pb2.EmbedRequest(inputs=text, normalize=True)

    embeddings = []
    async for response in stub.EmbedStream(batch(texts)):
        embeddings.append(response.embeddings)

    return np.array(embeddings, dtype=np.float16)
