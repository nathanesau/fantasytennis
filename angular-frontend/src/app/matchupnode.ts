import { Matchup } from './matchup'

export interface MatchupNode {
  data: Matchup;
  left: MatchupNode;
  right: MatchupNode;
}
