import { Component, Input, OnInit, ViewEncapsulation } from '@angular/core';
import { map } from 'rxjs/operators';
import { Matchup } from '../matchup';
import { MatchupNode } from '../matchupnode';
import { MatchupsService } from '../matchups.service';

@Component({
  selector: 'app-bracket',
  templateUrl: './bracket.component.html',
  styleUrls: ['./bracket.component.css'],
  encapsulation: ViewEncapsulation.None,
})
export class BracketComponent implements OnInit {
  @Input() tournamentName: string;
  @Input() tournamentStartDate: string;
  matchups: Matchup[];
  htmlBracket: string;
  winnerIcon = '<img src="assets/img/check.svg" width="12" />';

  constructor(private matchupsService: MatchupsService) {}

  ngOnInit() {
    this.generateHtmlBracket();
  }

  private fillNodes(
    root: MatchupNode,
    curr_depth: number,
    target_depth: number,
    nodes: MatchupNode[]
  ) {
    if (curr_depth == target_depth) {
      nodes.push(root);
    } else if (curr_depth < target_depth) {
      this.fillNodes(root.left, curr_depth + 1, target_depth, nodes);
      this.fillNodes(root.right, curr_depth + 1, target_depth, nodes);
    }
  }

  private getNodes(root: MatchupNode, target_depth: number): MatchupNode[] {
    var nodes = [];
    this.fillNodes(root, 1, target_depth, nodes);
    return nodes;
  }

  private addMissingMatchups() {
    var numMatchups = this.matchups.length;
    if (
      numMatchups != 127 &&
      numMatchups != 63 &&
      numMatchups != 31 &&
      numMatchups != 15 &&
      numMatchups != 7
    ) {
      var numFirstRoundMatchups = 0;
      for (var matchup of this.matchups) {
        if (matchup.round == 1) {
          numFirstRoundMatchups += 1;
        }
      }
      var numMissingMatchups = numFirstRoundMatchups * 2 - numMatchups - 1;
    }
  }

  private getMatchupTree(): MatchupNode {
    this.addMissingMatchups();
    var matchups = this.matchups;
    var root = {
      data: {
        player1: matchups[matchups.length - 1].player1,
        player2: matchups[matchups.length - 1].player2,
        round: matchups[matchups.length - 1].round,
        winner: matchups[matchups.length - 1].winner,
      },
      left: null,
      right: null,
    };
    var round_size = 1;
    var depth = 1;
    var index = matchups.length;
    while (round_size < matchups.length / 2) {
      var nodes = this.getNodes(root, depth);
      index = index - round_size * 2;
      for (var node of nodes) {
        node.left = {
          data: {
            player1: matchups[index - 1].player1,
            player2: matchups[index - 1].player2,
            round: matchups[index - 1].round,
            winner: matchups[index - 1].winner,
          },
          left: null,
          right: null,
        };
        node.right = {
          data: {
            player1: matchups[index].player1,
            player2: matchups[index].player2,
            round: matchups[index].round,
            winner: matchups[index].winner,
          },
          left: null,
          right: null,
        };
        index += 2;
      }
      index = index - round_size * 2;
      round_size *= 2;
      depth += 1;
    }
    return root;
  }

  private pad(name: string, nameLength: number): string {
    return name + '&nbsp'.repeat(nameLength - name.length);
  }

  private getIcon(winner: boolean): string {
    if(winner) {
      return this.winnerIcon;
    }
    return '';
  }

  private getNodeHtml(node: MatchupNode, nameLength: number): string {
    return (
      '<div class="vtb-item-players">\n' +
      '<div>\n' +
      '<div class="vtb-player vtb-player1 defeated player">\n' +
      `<span class="player1"> ${this.pad(node.data.player1, nameLength)} </span>\n` +
      `<span class="icon"> ${this.getIcon(node.data.player1 === node.data.winner)} </span>\n` +
      '</div>\n' +
      '<div class="vtb-player vtb-player2 winner player">\n' +
      `<span class="player2"> ${this.pad(node.data.player2, nameLength)} </span>\n` +
      `<span class="icon"> ${this.getIcon(node.data.player2 === node.data.winner)} </span>\n` +
      '</div>\n' +
      '</div>\n' +
      '</div>\n'
    );
  }

  private getHtml(root: MatchupNode, nameLength: number): string {
    if (root.left == null && root.right == null) {
      return this.getNodeHtml(root, nameLength);
    }

    return (
      '<div class="vtb-item">\n' +
      '<div class="vtb-item-parent"> \n' +
      this.getNodeHtml(root, nameLength) +
      '</div>\n' +
      '<div class="vtb-item-children">\n' +
      '<div class="vtb-item-child">\n' +
      this.getHtml(root.left, nameLength) +
      '</div>\n' +
      '<div class="vtb-item-child">\n' +
      this.getHtml(root.right, nameLength) +
      '</div>\n' +
      '</div>\n' +
      '</div>\n'
    );
  }

  generateHtmlBracket(): void {
    this.matchupsService
      .getMatchups(this.tournamentName, this.tournamentStartDate)
      .subscribe((matchups) => {
        this.matchups = matchups;
        var root = this.getMatchupTree();
        var nameLength = Math.max(
          ...this.matchups.map((matchup) =>
            Math.max(matchup.player1.length, matchup.player2.length)
          )
        );
        this.htmlBracket = this.getHtml(root, nameLength);
      });
  }

  // TODO event handlers
  highlightPlayer(): void {
    console.log('highlight player');
  }
}
