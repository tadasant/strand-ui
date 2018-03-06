import {GetTopicsTopicsFragment, GetTopicsUserFragment} from '../../schema/graphql-types';
import * as casual from 'casual';

casual.define('originalPoster', (): GetTopicsUserFragment => ({
  id: casual.word,
  alias: casual.username,
}));

// TODO contribute custom generated types to casual
const fakeOriginalPoster = (casual as any).originalPoster;

casual.define('topic', (): GetTopicsTopicsFragment => ({
  id: casual.word,
  title: casual.title,
  description: casual.description,
  tags: [
    {
      name: casual.word,
    },
    {
      name: casual.word,
    }
  ],
  originalPoster: fakeOriginalPoster,
  discussion: {
    status: casual.word,
    participants: [
      fakeOriginalPoster,
      {
        id: casual.word,
        alias: casual.word,
      }
    ]
  }
}));

export const topicFaker = (casual as any).topic;