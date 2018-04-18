import * as React from 'react';
import {Fragment, ReactType} from 'react';
import Paper from 'material-ui/Paper';
import Typography from 'material-ui/Typography';

/*
  Defaults:

  root - Root container element that contains the rendered markdown
  text - Text rendered inside of other elements, such as paragraphs
    Probably don't want to edit this, as it affects everything within e.g. paragraph
  break - Hard-break (<br>)
  paragraph - Paragraph (<p>)
  emphasis - Emphasis (<em>)
  strong - Strong/bold (<strong>)
  thematicBreak - Horizontal rule / thematic break (<hr>)
  blockquote - Block quote (<blockquote>)
  delete - Deleted/strike-through (<del>)
  link - Link (<a>)
  image - Image (<img>)
  linkReference - Link (through a reference) (<a>)
  imageReference - Image (through a reference) (<img>)
  table - Table (<table>)
  tableHead - Table head (<thead>)
  tableBody - Table body (<tbody>)
  tableRow - Table row (<tr>)
  tableCell - Table cell (<td>/<th>)
  list - List (<ul>/<ol>)
  listItem - List item (<li>)
  definition - Definition (not rendered by default)
  heading - Heading (<h1>-<h6>)
  inlineCode - Inline code (<code>)
  code - Block of code (<pre><code>)
  html - HTML node (Best-effort rendering)
 */

const renderers: {[nodeType: string]: ReactType} = {
  'root': props => <Paper><div style={{padding: '1%'}}>{props.children}</div></Paper>,
  'paragraph': ({children}) => <Fragment><Typography>{children}</Typography><br /></Fragment>,
  'inlineCode': (props) => <code style={{color: 'red', borderStyle: 'solid', borderWidth: '1px', borderColor: 'lightgrey'}}>{props.children}</code>,
  'code': (props) => <pre style={{backgroundColor: 'lightgray', borderStyle: 'solid', borderWidth: '1px'}}><code>{props.value}</code></pre>,
  'listItem': (props) => (
    <li>
      {props.checked !== null
        ? <input type="checkbox" readOnly checked={props.checked} />
        : null}
      <Typography>{props.children}</Typography>
    </li>
  )
};

export default renderers;