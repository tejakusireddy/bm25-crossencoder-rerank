function(obj) {
    if (obj instanceof Cell) {
      return {
        inside: obj.inside
      };
    } else {
      return {
        back : serialize(obj.back),
        front : serialize(obj.front),
        plane: obj.plane,
        shp: obj.shp,
        complemented: obj.complemented,
      };
    }
  }