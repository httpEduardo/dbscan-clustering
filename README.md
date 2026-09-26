# Dbscan Clustering

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)

Dbscan Clustering groups 2D points using DBSCAN density clustering.

## Quick start

```bash
python -m dbscan_clustering.server --port 5173
```

Open http://localhost:5173

## API

- POST `/api/cluster` `{ "points": [[1,2],[2,2]], "eps": 1.2, "min_pts": 3 }`

