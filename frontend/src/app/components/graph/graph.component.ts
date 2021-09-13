import { AfterContentInit, Component, OnInit } from '@angular/core';
import * as d3 from 'd3';
import { Observable, Subject } from 'rxjs';
import { delay } from 'rxjs/operators';
import { ApiService, initialData } from '../../services/api.service';

@Component({
  selector: 'app-graph',
  templateUrl: './graph.component.html',
  styleUrls: ['./graph.component.scss'],
})
export class GraphComponent implements OnInit, AfterContentInit {
  private datum$: Observable<any>;
  focusedNodeText$ = new Subject<string>();
  isFocusedVisible = false;

  constructor(private api: ApiService) {
    this.datum$ = this.api.datum$;
  }

  findNode(id) {
    for (const i in this.nodes) {
      if (this.nodes[i]['id'] === id) {
        return this.nodes[i];
      }
    }
    return id;
  }

  ngOnInit() {
    this.datum$.pipe(delay(1000)).subscribe((data) => {
      if (!data.links || !data.nodes) {
        return;
      }
      const links = data.links.map((d) => Object.create(d));
      const nodes = data.nodes.map((d) => Object.create(d));
      this.nodes = this.nodes.concat(nodes);
      links.forEach((link) => {
        link.source = this.findNode(link.source);
        link.target = this.findNode(link.target);
      });
      this.links = this.links.concat(links);

      this.update(this.nodes, this.links);
    });

    this.api.getGraph();
    setTimeout(() => {
      this.api.startListening();
    }, 2000);
  }

  private links = initialData.links.map((d) => Object.create(d));
  private nodes = initialData.nodes.map((d) => Object.create(d));

  width = 960;
  height = 780;

  private simulation;
  private svg;
  private link;
  private node;

  private colors = d3.scaleOrdinal(d3.schemeCategory10);

  ngAfterContentInit() {
    this.simulation = d3
      .forceSimulation(this.nodes)
      .force(
        'link',
        d3.forceLink(this.links).id((d: any) => d.id),
      )
      .force('charge', d3.forceManyBody())
      .force('center', d3.forceCenter(this.width / 2, this.height / 2))
      .force('x', d3.forceX().strength(0.05))
      .force('y', d3.forceY().strength(0.05));

    this.svg = d3
      .select('#graphContainer')
      .append('svg')
      .attr('width', this.width) // "100%" also works
      .attr('height', this.height);

    this.simulation.on('tick', () => {
      this.node.attr('cx', (d) => d.x).attr('cy', (d) => d.y);
      this.link
        .attr('x1', (d) => d.source.x)
        .attr('y1', (d) => d.source.y)
        .attr('x2', (d) => d.target.x)
        .attr('y2', (d) => d.target.y);
    });

    this.link = this.svg
      .append('g')
      .attr('stroke', '#999')
      .attr('stroke-opacity', 0.6)
      .selectAll('line')
      .data(this.links)
      .join('line')
      .attr('id', (d: any) => d.source.id + '-' + d.target.id)
      .attr('stroke-width', (d: any) => Math.sqrt(d.value));

    this.node = this.svg
      .append('g')
      .attr('stroke', '#fff')
      .attr('stroke-width', 1.5)
      .selectAll('circle')
      .data(this.nodes)
      .join('circle')
      .attr('r', (d: any) => d.radius)
      .style('fill', (d: any) => d.color);
  }

  private update(nodes, links) {
    // Update existing nodes
    this.node.selectAll('circle').style('fill', (d) => this.colors(d.id));

    // Remove old nodes
    this.node.exit().remove();

    // Add new nodes
    this.node = this.node.data(nodes, (d) => d.id);
    this.node = this.node
      .enter()
      .append('circle')
      .attr('text', (d: any) => d.text)
      .attr('r', (d: any) => d.radius)
      .style('fill', (d: any) => d.color)
      .on('mouseover', (d) => {
        const text = d.srcElement.getAttribute('text');
        this.focusedNodeText$.next(text);
        this.isFocusedVisible = true;
      })
      .on('mouseout', () => {
        this.isFocusedVisible = false;
      })
      .merge(this.node);

    this.link = this.link.data(links, (d: any) => {
      return d.source.id + '-' + d.target.id;
    });

    // Remove old links
    this.link.exit().remove();

    this.link = this.link
      .enter()
      .append('line')
      .attr('id', (d: any) => d.source.id + '-' + d.target.id)
      .attr('stroke', '#999')
      .attr('stroke-opacity', 0.6)
      .attr('stroke-width', (d: any) => Math.sqrt(d.value))
      .merge(this.link);

    try {
      this.simulation
        .nodes(this.nodes)
        .force('link', d3.forceLink(this.links))
        .force(
          'collide',
          d3
            .forceCollide()
            .strength(1)
            .radius(function (d) {
              return 20;
            })
            .iterations(1),
        )
        .force('charge', d3.forceManyBody())
        .force('center', d3.forceCenter(this.width / 2, this.height / 2));
    } catch (err) {
      console.log('err', err);
    }

    this.simulation.on('tick', () => {
      this.node.attr('cx', (d) => d.x).attr('cy', (d) => d.y);
      this.link
        .attr('x1', (d) => d.source.x)
        .attr('y1', (d) => d.source.y)
        .attr('x2', (d) => d.target.x)
        .attr('y2', (d) => d.target.y);
    });
    this.simulation.alphaTarget(0.1).restart();
  }
}
