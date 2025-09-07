function(inlines) {
  var m;
  if ((m = this.match(reMain))) {
    inlines.push({ t: 'Str', c: m });
    return m.length;
  } else {
    return 0;
  }
}