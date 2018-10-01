/**
 * Style-Utils defines a set of classes that provide css styling functionality.
 */

export class HexHelpers {

  /**
   * Calculates a color gradient between `startColor` and `endColor`
   * @param {number} value The value to be placed on a range between `max` and `min`
   * @param {number} min The minimum value to be accepted, corresponding to `startColor`
   * @param {number} max The maximum value to be accepted, corresponding to `endColor`
   * @param {string} startColor The color to display if `value` <= min
   * @param {string} endColor The color to display if `value` >= max
   * @returns {string} A 6-character hex color representing a point on the gradient between `startColor` and `endColor`
   */
  static calculateColorGradient(value: number, min: number, max: number, startColor: string, endColor: string): string {
    if (value >= max) {
      return endColor;
    }
    if (value <= min) {
      return startColor;
    }

    // Ending hex codes for the start and end colors
    const [r1, g1, b1] = HexHelpers.hexToRGB(startColor);
    const [r2, g2, b2] = HexHelpers.hexToRGB(endColor);
    const percentage = value / (max - min);

    let dr = r2 + (1 - percentage) * (r1 - r2);
    let dg = g2 + (1 - percentage) * (g1 - g2);
    let db = b2 + (1 - percentage) * (b1 - b2);

    const padWithZero = function(num: number) {
      let s = num.toString(16);
      if (s.length === 1) {
        s = '0' + s;
      }
      return s
    };

    const rStr = padWithZero(Math.round(dr));
    const gStr = padWithZero(Math.round(dg));
    const bStr = padWithZero(Math.round(db));
    return '#' + rStr + gStr + bStr;
  }

  /**
   * Converts a 6-letter hex color code to an array with three corresponding RGB values
   * @param {string} hexCode A 6-letter hex color code prefixed with a '#'
   * @returns {Array<number>} An array of three numbers denoting Red, Green, and Blue respectively
   */
  private static hexToRGB(hexCode: string): Array<number> {
    const r = hexCode.substring(1, 3);
    const g = hexCode.substring(3, 5);
    const b = hexCode.substring(5);
    return [parseInt(r, 16), parseInt(g, 16), parseInt(b, 16)];
  }

}

