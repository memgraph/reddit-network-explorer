<h1 align="center">
 🔍 Reddit Network Explorer 🔍
</h1>

<p align="center">
  <a href="https://github.com/memgraph/reddit-network-explorer/LICENSE">
    <img src="https://img.shields.io/github/license/memgraph/reddit-network-explorer" alt="license" title="license"/>
  </a>
  <a href="https://github.com/memgraph/reddit-network-explorer">
    <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="build" title="build"/>
  </a>
  <a href="#contributors-">
    <img src="https://img.shields.io/badge/all_contributors-3-green.svg?style=flat" />
  </a>
</p>

<p align="center">
    <a href="https://twitter.com/intent/follow?screen_name=memgraphdb"><img
    src="https://img.shields.io/twitter/follow/memgraphdb.svg?label=Follow%20@memgraphdb"
    alt="Follow @memgraphdb" /></a>
</p>

<p align="center">
  <a href="https://github.com/memgraph/reddit-network-explorer">
    <img src="https://public-assets.memgraph.com/github-readme-images/reddit-network-explorer.png" 
         alt="reddit-network-explorer" 
         title="reddit-network-explorer"
         style="width: 80%"/>
  </a>
</p>

The **Reddit Network Explorer** is a web application that lets you visualize a
subreddit in real-time as well as perform sentiment analysis and different
network analysis algorithms.

## 📚 Data model

<img src="https://public-assets.memgraph.com/reddit-network-explorer/memgraph-blog-reddit-graph-data-model.png" 
         alt="reddit-network-explorer" 
         title="reddit-network-explorer"
         style="width: 80%"/>
    
## 👉 Try it out!

* The demo application - **[reddit.memgraph.com](http://reddit.memgraph.com/)**
  (**Not deployed yet!**)
* The Memgraph instance - **bolt://reddit.memgraph.com:7687**

To explore the data, please download [Memgraph
Lab](https://memgraph.com/product/lab). The endpoint is `reddit.memgraph.com`
and the port is '7687'.

## 🖥️ Run the app locally

The simplest way of running the app locally is by using [Docker
Compose](https://docs.docker.com/compose/install/). Just run the following
commands in the root directory:

```
docker-compose build
docker-compose up backend-app
docker-compose up frontend-app
docker-compose up reddit-stream
```

## ❔ Find out more about Memgraph

Memgraph makes creating real-time streaming graph applications accessible to
every developer. Spin up an instance, consume data directly from Kafka, and
build on top of everything from super-fast graph queries to PageRank and
Community Detection.
* [Memgraph Docs](https://docs.memgraph.com)
* [Memgraph Download](https://memgraph.com/download)

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/antonio2368"><img src="https://avatars.githubusercontent.com/u/17751307?v=4" width="100px;" alt=""/><br /><sub><b>Antonio Andelic</b></sub></a></td>
    <td align="center"><a href="https://github.com/cizl"><img src="https://avatars.githubusercontent.com/u/3769376?v=4" width="100px;" alt=""/><br /><sub><b>David Lozic</b></sub></a></td>
    <td align="center"><a href="https://github.com/g-despot"><img src="https://avatars.githubusercontent.com/u/66276597?v=4" width="100px;" alt=""/><br /><sub><b>Ivan Despot</b></sub></a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!!
