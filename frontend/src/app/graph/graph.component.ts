import { AfterContentInit, Component, OnInit } from '@angular/core';
import * as d3 from 'd3';
import { Observable } from 'rxjs';
import { delay } from 'rxjs/operators';
import { ApiService, mockData } from '../services/api.service.mock';

@Component({
  selector: 'app-graph',
  templateUrl: './graph.component.html',
  styleUrls: ['./graph.component.scss']
})
export class GraphComponent implements OnInit, AfterContentInit {

  private data$: Observable<any>;

  constructor(private api: ApiService) {
    this.data$ = this.api.data$;
  }

  findNode(id) {
    //return this.data.nodes.filter((node) => node.id === id)[0];
    for (var i in this.nodes) {
      if (this.nodes[i]["id"] === id) return this.nodes[i];
    }
  };

  ngOnInit() {
    this.data$.pipe(delay(1000)).subscribe(data => {
      this.data = data;
      if (!data.links || !data.nodes) return;
      const links = data.links.map(d => Object.create(d));
      const nodes = data.nodes.map(d => Object.create(d));
      this.nodes = nodes;
      links.forEach((link) => {
        link.source = this.findNode(link.source);
        link.target = this.findNode(link.target);
      });

      this.update(nodes, links);

      this.simulation.nodes(nodes)
        .force("collide", d3.forceCollide().strength(1).radius(function(d){ return 10; }).iterations(1));
    })
    this.api.startPolling();
  }


  private data = mockData;
  private links = this.data.links.map(d => Object.create(d));
  private nodes = this.data.nodes.map(d => Object.create(d));

  width = 960;
  height = 780;

  private simulation;
  private svg;
  private link;
  private node;
  private drag;

  private colors = d3.scaleOrdinal(d3.schemeCategory10);

	ngAfterContentInit() {
    this.simulation = d3.forceSimulation(this.nodes)
      .force("link", d3.forceLink(this.links).id((d: any) => d.id))
      .force("charge", d3.forceManyBody())
      .force("center", d3.forceCenter(this.width / 2, this.height / 2))
      .force("x", d3.forceX())
      .force("y", d3.forceY());

    this.svg = d3.select("#graphContainer")
      .append('svg')
      .attr("width", this.width) // "100%" also works
      .attr("height", this.height)

    // init D3 drag support
    this.drag = d3.drag()
    .on('start', (event: any, d: any) => {
      if (!event.active) {
        this.simulation.alphaTarget(0.3).restart();
      }
      d.fx = d.x;
      d.fy = d.y;
    })
    .on('drag', (event: any, d: any) => {
      d.fx = event.x;
      d.fy = event.y;
    })
    .on('end', (event: any, d: any) => {
      if (!event.active) {
        this.simulation.alphaTarget(0.3);
      }
      d.fx = null;
      d.fy = null;
    });

    this.simulation.on("tick", () => {
      this.link
          .attr("x1", d => d.source.x)
          .attr("y1", d => d.source.y)
          .attr("x2", d => d.target.x)
          .attr("y2", d => d.target.y);
      this.node
          .attr("cx", d => d.x)
          .attr("cy", d => d.y);
    });

    this.link = this.svg.append("g")
      .attr("stroke", "#999")
      .attr("stroke-opacity", 0.6)
      .selectAll("line")
      .data(this.links)
      .join("line")
      .attr('id', (d: any) => d.source.id + '-' + d.target.id)
      .attr("stroke-width", (d: any) => Math.sqrt(d.value))

    this.node = this.svg.append("g")
      .attr("stroke", "#fff")
      .attr("stroke-width", 1.5)
      .selectAll("circle")
      .data(this.nodes)
      .join("circle")
      .attr("r", 5)
      .style("fill", (d: any) => this.colors(d.group))
      .call(this.drag);

  }

  private update(nodes, links) {
    this.link = this.link.data(links, (d: any) => d.source.id + '-' + d.target.id)

    // Remove old links
    this.link.exit().remove();

    this.link = this.link.enter().append('line')
      .attr('id', (d: any) => d.source.id + '-' + d.target.id)
      .attr("stroke", "#999")
      .attr("stroke-opacity", 0.6)
      .attr("stroke-width", (d: any) => Math.sqrt(d.value))
      //.attr("stroke", "black")
      .merge(this.link);


    // Update existing nodes
    this.node.selectAll('circle')
      .style('fill', (d) => this.colors(d.id));

    // Remove old nodes
    this.node.exit().remove();

    // Add new nodes
    this.node = this.node.data(nodes, (d) => d.id);
    this.node = this.node.enter().append('circle')
      .attr("r", 5)
      .style("fill", (d: any) => { return this.colors(d.group); })
      .merge(this.node);

  }

}
