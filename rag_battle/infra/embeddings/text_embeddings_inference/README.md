You can regenerate tei_pb2.py and tei_pb2_grpc.py using:

```bash
pip install grpcio grpcio-tools
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. tei.proto
```

Update tei_pb2_grpc.py:
replace

```python
import tei_pb2 as tei__pb2
```

with

```text
import rag_battle.infra.embeddings.text_embeddings_inference.tei.tei_pb2 as tei__pb2
```