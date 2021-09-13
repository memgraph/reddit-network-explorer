// Returns D3 compatible styles for specific node type.
export function getStyle(type, sentiment) {
  if (type === 'COMMENT') {
    const radius = 7;
    let color = '#989898';
    if (sentiment === -1) {
      color = '#ff0000';
    }
    if (sentiment === 1) {
      color = '#00ff00';
    }
    return { color, radius };
  }
  if (type === 'REDDITOR') {
    return { color: '#0000ff', radius: 5 };
  }
  if (type === 'SUBMISSION') {
    const radius = 12;
    let color = '#585858';
    if (sentiment === -1) {
      color = '#F2543D';
    }
    if (sentiment === 1) {
      color = '#38C477';
    }
    return { color, radius };
  }
  return { color: '#ef42f5', radius: 3 };
}
