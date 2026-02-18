from fastapi import FastAPI, Body
from typing import Dict, List
from collections import defaultdict, deque
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Ping": "Pong"}


@app.post("/pipelines/parse")
def parse_pipeline(pipeline: Dict = Body(...)):
    nodes = pipeline.get("nodes", [])
    edges = pipeline.get("edges", [])

    num_nodes = len(nodes)
    num_edges = len(edges)

    graph = defaultdict(list)
    in_degree = defaultdict(int)

    for node in nodes:
        in_degree[node["id"]] = 0

    for edge in edges:
        source = edge["source"]
        target = edge["target"]

        graph[source].append(target)
        in_degree[target] += 1

    queue = deque([node for node in in_degree if in_degree[node] == 0])
    visited_count = 0

    while queue:
        node = queue.popleft()
        visited_count += 1

        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    is_dag = visited_count == num_nodes

    return {
        "num_nodes": num_nodes,
        "num_edges": num_edges,
        "is_dag": is_dag
    }
