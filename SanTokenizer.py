import bisect
from logging import raiseExceptions
import unicodedata


def _read_blocks():
    # https://www.unicode.org/Public/UCD/latest/ucd/Blocks.txt
    blocks = []
    for line in open("Blocks.txt"):
        line = line.strip()
        if not line or line[0] == '#':
            continue
        w = line.split('; ')
        name = w[1].strip()
        a, b = w[0].split('..')
        m = int(a, 16)
        n = int(b, 16)
        blocks.append([m, n, name])
        print(f"[{hex(m)},{hex(n)},'{name}'],")
    # print("==blocks==")


_blocks = [
    [0x0, 0x7f, 'Basic Latin'],
    [0x80, 0xff, 'Latin-1 Supplement'],
    [0x100, 0x17f, 'Latin Extended-A'],
    [0x180, 0x24f, 'Latin Extended-B'],
    [0x250, 0x2af, 'IPA Extensions'],
    [0x2b0, 0x2ff, 'Spacing Modifier Letters'],
    [0x300, 0x36f, 'Combining Diacritical Marks'],
    [0x370, 0x3ff, 'Greek and Coptic'],
    [0x400, 0x4ff, 'Cyrillic'],
    [0x500, 0x52f, 'Cyrillic Supplement'],
    [0x530, 0x58f, 'Armenian'],
    [0x590, 0x5ff, 'Hebrew'],
    [0x600, 0x6ff, 'Arabic'],
    [0x700, 0x74f, 'Syriac'],
    [0x750, 0x77f, 'Arabic Supplement'],
    [0x780, 0x7bf, 'Thaana'],
    [0x7c0, 0x7ff, 'NKo'],
    [0x800, 0x83f, 'Samaritan'],
    [0x840, 0x85f, 'Mandaic'],
    [0x860, 0x86f, 'Syriac Supplement'],
    [0x870, 0x89f, 'Arabic Extended-B'],
    [0x8a0, 0x8ff, 'Arabic Extended-A'],
    [0x900, 0x97f, 'Devanagari'],
    [0x980, 0x9ff, 'Bengali'],
    [0xa00, 0xa7f, 'Gurmukhi'],
    [0xa80, 0xaff, 'Gujarati'],
    [0xb00, 0xb7f, 'Oriya'],
    [0xb80, 0xbff, 'Tamil'],
    [0xc00, 0xc7f, 'Telugu'],
    [0xc80, 0xcff, 'Kannada'],
    [0xd00, 0xd7f, 'Malayalam'],
    [0xd80, 0xdff, 'Sinhala'],
    [0xe00, 0xe7f, 'Thai'],
    [0xe80, 0xeff, 'Lao'],
    [0xf00, 0xfff, 'Tibetan'],
    [0x1000, 0x109f, 'Myanmar'],
    [0x10a0, 0x10ff, 'Georgian'],
    [0x1100, 0x11ff, 'Hangul Jamo'],
    [0x1200, 0x137f, 'Ethiopic'],
    [0x1380, 0x139f, 'Ethiopic Supplement'],
    [0x13a0, 0x13ff, 'Cherokee'],
    [0x1400, 0x167f, 'Unified Canadian Aboriginal Syllabics'],
    [0x1680, 0x169f, 'Ogham'],
    [0x16a0, 0x16ff, 'Runic'],
    [0x1700, 0x171f, 'Tagalog'],
    [0x1720, 0x173f, 'Hanunoo'],
    [0x1740, 0x175f, 'Buhid'],
    [0x1760, 0x177f, 'Tagbanwa'],
    [0x1780, 0x17ff, 'Khmer'],
    [0x1800, 0x18af, 'Mongolian'],
    [0x18b0, 0x18ff, 'Unified Canadian Aboriginal Syllabics Extended'],
    [0x1900, 0x194f, 'Limbu'],
    [0x1950, 0x197f, 'Tai Le'],
    [0x1980, 0x19df, 'New Tai Lue'],
    [0x19e0, 0x19ff, 'Khmer Symbols'],
    [0x1a00, 0x1a1f, 'Buginese'],
    [0x1a20, 0x1aaf, 'Tai Tham'],
    [0x1ab0, 0x1aff, 'Combining Diacritical Marks Extended'],
    [0x1b00, 0x1b7f, 'Balinese'],
    [0x1b80, 0x1bbf, 'Sundanese'],
    [0x1bc0, 0x1bff, 'Batak'],
    [0x1c00, 0x1c4f, 'Lepcha'],
    [0x1c50, 0x1c7f, 'Ol Chiki'],
    [0x1c80, 0x1c8f, 'Cyrillic Extended-C'],
    [0x1c90, 0x1cbf, 'Georgian Extended'],
    [0x1cc0, 0x1ccf, 'Sundanese Supplement'],
    [0x1cd0, 0x1cff, 'Vedic Extensions'],
    [0x1d00, 0x1d7f, 'Phonetic Extensions'],
    [0x1d80, 0x1dbf, 'Phonetic Extensions Supplement'],
    [0x1dc0, 0x1dff, 'Combining Diacritical Marks Supplement'],
    [0x1e00, 0x1eff, 'Latin Extended Additional'],
    [0x1f00, 0x1fff, 'Greek Extended'],
    [0x2000, 0x206f, 'General Punctuation'],
    [0x2070, 0x209f, 'Superscripts and Subscripts'],
    [0x20a0, 0x20cf, 'Currency Symbols'],
    [0x20d0, 0x20ff, 'Combining Diacritical Marks for Symbols'],
    [0x2100, 0x214f, 'Letterlike Symbols'],
    [0x2150, 0x218f, 'Number Forms'],
    [0x2190, 0x21ff, 'Arrows'],
    [0x2200, 0x22ff, 'Mathematical Operators'],
    [0x2300, 0x23ff, 'Miscellaneous Technical'],
    [0x2400, 0x243f, 'Control Pictures'],
    [0x2440, 0x245f, 'Optical Character Recognition'],
    [0x2460, 0x24ff, 'Enclosed Alphanumerics'],
    [0x2500, 0x257f, 'Box Drawing'],
    [0x2580, 0x259f, 'Block Elements'],
    [0x25a0, 0x25ff, 'Geometric Shapes'],
    [0x2600, 0x26ff, 'Miscellaneous Symbols'],
    [0x2700, 0x27bf, 'Dingbats'],
    [0x27c0, 0x27ef, 'Miscellaneous Mathematical Symbols-A'],
    [0x27f0, 0x27ff, 'Supplemental Arrows-A'],
    [0x2800, 0x28ff, 'Braille Patterns'],
    [0x2900, 0x297f, 'Supplemental Arrows-B'],
    [0x2980, 0x29ff, 'Miscellaneous Mathematical Symbols-B'],
    [0x2a00, 0x2aff, 'Supplemental Mathematical Operators'],
    [0x2b00, 0x2bff, 'Miscellaneous Symbols and Arrows'],
    [0x2c00, 0x2c5f, 'Glagolitic'],
    [0x2c60, 0x2c7f, 'Latin Extended-C'],
    [0x2c80, 0x2cff, 'Coptic'],
    [0x2d00, 0x2d2f, 'Georgian Supplement'],
    [0x2d30, 0x2d7f, 'Tifinagh'],
    [0x2d80, 0x2ddf, 'Ethiopic Extended'],
    [0x2de0, 0x2dff, 'Cyrillic Extended-A'],
    [0x2e00, 0x2e7f, 'Supplemental Punctuation'],
    [0x2e80, 0x2eff, 'CJK Radicals Supplement'],
    [0x2f00, 0x2fdf, 'Kangxi Radicals'],
    [0x2ff0, 0x2fff, 'Ideographic Description Characters'],
    [0x3000, 0x303f, 'CJK Symbols and Punctuation'],
    [0x3040, 0x309f, 'Hiragana'],
    [0x30a0, 0x30ff, 'Katakana'],
    [0x3100, 0x312f, 'Bopomofo'],
    [0x3130, 0x318f, 'Hangul Compatibility Jamo'],
    [0x3190, 0x319f, 'Kanbun'],
    [0x31a0, 0x31bf, 'Bopomofo Extended'],
    [0x31c0, 0x31ef, 'CJK Strokes'],
    [0x31f0, 0x31ff, 'Katakana Phonetic Extensions'],
    [0x3200, 0x32ff, 'Enclosed CJK Letters and Months'],
    [0x3300, 0x33ff, 'CJK Compatibility'],
    [0x3400, 0x4dbf, 'CJK Unified Ideographs Extension A'],
    [0x4dc0, 0x4dff, 'Yijing Hexagram Symbols'],
    [0x4e00, 0x9fff, 'CJK Unified Ideographs'],
    [0xa000, 0xa48f, 'Yi Syllables'],
    [0xa490, 0xa4cf, 'Yi Radicals'],
    [0xa4d0, 0xa4ff, 'Lisu'],
    [0xa500, 0xa63f, 'Vai'],
    [0xa640, 0xa69f, 'Cyrillic Extended-B'],
    [0xa6a0, 0xa6ff, 'Bamum'],
    [0xa700, 0xa71f, 'Modifier Tone Letters'],
    [0xa720, 0xa7ff, 'Latin Extended-D'],
    [0xa800, 0xa82f, 'Syloti Nagri'],
    [0xa830, 0xa83f, 'Common Indic Number Forms'],
    [0xa840, 0xa87f, 'Phags-pa'],
    [0xa880, 0xa8df, 'Saurashtra'],
    [0xa8e0, 0xa8ff, 'Devanagari Extended'],
    [0xa900, 0xa92f, 'Kayah Li'],
    [0xa930, 0xa95f, 'Rejang'],
    [0xa960, 0xa97f, 'Hangul Jamo Extended-A'],
    [0xa980, 0xa9df, 'Javanese'],
    [0xa9e0, 0xa9ff, 'Myanmar Extended-B'],
    [0xaa00, 0xaa5f, 'Cham'],
    [0xaa60, 0xaa7f, 'Myanmar Extended-A'],
    [0xaa80, 0xaadf, 'Tai Viet'],
    [0xaae0, 0xaaff, 'Meetei Mayek Extensions'],
    [0xab00, 0xab2f, 'Ethiopic Extended-A'],
    [0xab30, 0xab6f, 'Latin Extended-E'],
    [0xab70, 0xabbf, 'Cherokee Supplement'],
    [0xabc0, 0xabff, 'Meetei Mayek'],
    [0xac00, 0xd7af, 'Hangul Syllables'],
    [0xd7b0, 0xd7ff, 'Hangul Jamo Extended-B'],
    [0xd800, 0xdb7f, 'High Surrogates'],
    [0xdb80, 0xdbff, 'High Private Use Surrogates'],
    [0xdc00, 0xdfff, 'Low Surrogates'],
    [0xe000, 0xf8ff, 'Private Use Area'],
    [0xf900, 0xfaff, 'CJK Compatibility Ideographs'],
    [0xfb00, 0xfb4f, 'Alphabetic Presentation Forms'],
    [0xfb50, 0xfdff, 'Arabic Presentation Forms-A'],
    [0xfe00, 0xfe0f, 'Variation Selectors'],
    [0xfe10, 0xfe1f, 'Vertical Forms'],
    [0xfe20, 0xfe2f, 'Combining Half Marks'],
    [0xfe30, 0xfe4f, 'CJK Compatibility Forms'],
    [0xfe50, 0xfe6f, 'Small Form Variants'],
    [0xfe70, 0xfeff, 'Arabic Presentation Forms-B'],
    [0xff00, 0xffef, 'Halfwidth and Fullwidth Forms'],
    [0xfff0, 0xffff, 'Specials'],
    [0x10000, 0x1007f, 'Linear B Syllabary'],
    [0x10080, 0x100ff, 'Linear B Ideograms'],
    [0x10100, 0x1013f, 'Aegean Numbers'],
    [0x10140, 0x1018f, 'Ancient Greek Numbers'],
    [0x10190, 0x101cf, 'Ancient Symbols'],
    [0x101d0, 0x101ff, 'Phaistos Disc'],
    [0x10280, 0x1029f, 'Lycian'],
    [0x102a0, 0x102df, 'Carian'],
    [0x102e0, 0x102ff, 'Coptic Epact Numbers'],
    [0x10300, 0x1032f, 'Old Italic'],
    [0x10330, 0x1034f, 'Gothic'],
    [0x10350, 0x1037f, 'Old Permic'],
    [0x10380, 0x1039f, 'Ugaritic'],
    [0x103a0, 0x103df, 'Old Persian'],
    [0x10400, 0x1044f, 'Deseret'],
    [0x10450, 0x1047f, 'Shavian'],
    [0x10480, 0x104af, 'Osmanya'],
    [0x104b0, 0x104ff, 'Osage'],
    [0x10500, 0x1052f, 'Elbasan'],
    [0x10530, 0x1056f, 'Caucasian Albanian'],
    [0x10570, 0x105bf, 'Vithkuqi'],
    [0x10600, 0x1077f, 'Linear A'],
    [0x10780, 0x107bf, 'Latin Extended-F'],
    [0x10800, 0x1083f, 'Cypriot Syllabary'],
    [0x10840, 0x1085f, 'Imperial Aramaic'],
    [0x10860, 0x1087f, 'Palmyrene'],
    [0x10880, 0x108af, 'Nabataean'],
    [0x108e0, 0x108ff, 'Hatran'],
    [0x10900, 0x1091f, 'Phoenician'],
    [0x10920, 0x1093f, 'Lydian'],
    [0x10980, 0x1099f, 'Meroitic Hieroglyphs'],
    [0x109a0, 0x109ff, 'Meroitic Cursive'],
    [0x10a00, 0x10a5f, 'Kharoshthi'],
    [0x10a60, 0x10a7f, 'Old South Arabian'],
    [0x10a80, 0x10a9f, 'Old North Arabian'],
    [0x10ac0, 0x10aff, 'Manichaean'],
    [0x10b00, 0x10b3f, 'Avestan'],
    [0x10b40, 0x10b5f, 'Inscriptional Parthian'],
    [0x10b60, 0x10b7f, 'Inscriptional Pahlavi'],
    [0x10b80, 0x10baf, 'Psalter Pahlavi'],
    [0x10c00, 0x10c4f, 'Old Turkic'],
    [0x10c80, 0x10cff, 'Old Hungarian'],
    [0x10d00, 0x10d3f, 'Hanifi Rohingya'],
    [0x10e60, 0x10e7f, 'Rumi Numeral Symbols'],
    [0x10e80, 0x10ebf, 'Yezidi'],
    [0x10f00, 0x10f2f, 'Old Sogdian'],
    [0x10f30, 0x10f6f, 'Sogdian'],
    [0x10f70, 0x10faf, 'Old Uyghur'],
    [0x10fb0, 0x10fdf, 'Chorasmian'],
    [0x10fe0, 0x10fff, 'Elymaic'],
    [0x11000, 0x1107f, 'Brahmi'],
    [0x11080, 0x110cf, 'Kaithi'],
    [0x110d0, 0x110ff, 'Sora Sompeng'],
    [0x11100, 0x1114f, 'Chakma'],
    [0x11150, 0x1117f, 'Mahajani'],
    [0x11180, 0x111df, 'Sharada'],
    [0x111e0, 0x111ff, 'Sinhala Archaic Numbers'],
    [0x11200, 0x1124f, 'Khojki'],
    [0x11280, 0x112af, 'Multani'],
    [0x112b0, 0x112ff, 'Khudawadi'],
    [0x11300, 0x1137f, 'Grantha'],
    [0x11400, 0x1147f, 'Newa'],
    [0x11480, 0x114df, 'Tirhuta'],
    [0x11580, 0x115ff, 'Siddham'],
    [0x11600, 0x1165f, 'Modi'],
    [0x11660, 0x1167f, 'Mongolian Supplement'],
    [0x11680, 0x116cf, 'Takri'],
    [0x11700, 0x1174f, 'Ahom'],
    [0x11800, 0x1184f, 'Dogra'],
    [0x118a0, 0x118ff, 'Warang Citi'],
    [0x11900, 0x1195f, 'Dives Akuru'],
    [0x119a0, 0x119ff, 'Nandinagari'],
    [0x11a00, 0x11a4f, 'Zanabazar Square'],
    [0x11a50, 0x11aaf, 'Soyombo'],
    [0x11ab0, 0x11abf, 'Unified Canadian Aboriginal Syllabics Extended-A'],
    [0x11ac0, 0x11aff, 'Pau Cin Hau'],
    [0x11c00, 0x11c6f, 'Bhaiksuki'],
    [0x11c70, 0x11cbf, 'Marchen'],
    [0x11d00, 0x11d5f, 'Masaram Gondi'],
    [0x11d60, 0x11daf, 'Gunjala Gondi'],
    [0x11ee0, 0x11eff, 'Makasar'],
    [0x11fb0, 0x11fbf, 'Lisu Supplement'],
    [0x11fc0, 0x11fff, 'Tamil Supplement'],
    [0x12000, 0x123ff, 'Cuneiform'],
    [0x12400, 0x1247f, 'Cuneiform Numbers and Punctuation'],
    [0x12480, 0x1254f, 'Early Dynastic Cuneiform'],
    [0x12f90, 0x12fff, 'Cypro-Minoan'],
    [0x13000, 0x1342f, 'Egyptian Hieroglyphs'],
    [0x13430, 0x1343f, 'Egyptian Hieroglyph Format Controls'],
    [0x14400, 0x1467f, 'Anatolian Hieroglyphs'],
    [0x16800, 0x16a3f, 'Bamum Supplement'],
    [0x16a40, 0x16a6f, 'Mro'],
    [0x16a70, 0x16acf, 'Tangsa'],
    [0x16ad0, 0x16aff, 'Bassa Vah'],
    [0x16b00, 0x16b8f, 'Pahawh Hmong'],
    [0x16e40, 0x16e9f, 'Medefaidrin'],
    [0x16f00, 0x16f9f, 'Miao'],
    [0x16fe0, 0x16fff, 'Ideographic Symbols and Punctuation'],
    [0x17000, 0x187ff, 'Tangut'],
    [0x18800, 0x18aff, 'Tangut Components'],
    [0x18b00, 0x18cff, 'Khitan Small Script'],
    [0x18d00, 0x18d7f, 'Tangut Supplement'],
    [0x1aff0, 0x1afff, 'Kana Extended-B'],
    [0x1b000, 0x1b0ff, 'Kana Supplement'],
    [0x1b100, 0x1b12f, 'Kana Extended-A'],
    [0x1b130, 0x1b16f, 'Small Kana Extension'],
    [0x1b170, 0x1b2ff, 'Nushu'],
    [0x1bc00, 0x1bc9f, 'Duployan'],
    [0x1bca0, 0x1bcaf, 'Shorthand Format Controls'],
    [0x1cf00, 0x1cfcf, 'Znamenny Musical Notation'],
    [0x1d000, 0x1d0ff, 'Byzantine Musical Symbols'],
    [0x1d100, 0x1d1ff, 'Musical Symbols'],
    [0x1d200, 0x1d24f, 'Ancient Greek Musical Notation'],
    [0x1d2e0, 0x1d2ff, 'Mayan Numerals'],
    [0x1d300, 0x1d35f, 'Tai Xuan Jing Symbols'],
    [0x1d360, 0x1d37f, 'Counting Rod Numerals'],
    [0x1d400, 0x1d7ff, 'Mathematical Alphanumeric Symbols'],
    [0x1d800, 0x1daaf, 'Sutton SignWriting'],
    [0x1df00, 0x1dfff, 'Latin Extended-G'],
    [0x1e000, 0x1e02f, 'Glagolitic Supplement'],
    [0x1e100, 0x1e14f, 'Nyiakeng Puachue Hmong'],
    [0x1e290, 0x1e2bf, 'Toto'],
    [0x1e2c0, 0x1e2ff, 'Wancho'],
    [0x1e7e0, 0x1e7ff, 'Ethiopic Extended-B'],
    [0x1e800, 0x1e8df, 'Mende Kikakui'],
    [0x1e900, 0x1e95f, 'Adlam'],
    [0x1ec70, 0x1ecbf, 'Indic Siyaq Numbers'],
    [0x1ed00, 0x1ed4f, 'Ottoman Siyaq Numbers'],
    [0x1ee00, 0x1eeff, 'Arabic Mathematical Alphabetic Symbols'],
    [0x1f000, 0x1f02f, 'Mahjong Tiles'],
    [0x1f030, 0x1f09f, 'Domino Tiles'],
    [0x1f0a0, 0x1f0ff, 'Playing Cards'],
    [0x1f100, 0x1f1ff, 'Enclosed Alphanumeric Supplement'],
    [0x1f200, 0x1f2ff, 'Enclosed Ideographic Supplement'],
    [0x1f300, 0x1f5ff, 'Miscellaneous Symbols and Pictographs'],
    [0x1f600, 0x1f64f, 'Emoticons'],
    [0x1f650, 0x1f67f, 'Ornamental Dingbats'],
    [0x1f680, 0x1f6ff, 'Transport and Map Symbols'],
    [0x1f700, 0x1f77f, 'Alchemical Symbols'],
    [0x1f780, 0x1f7ff, 'Geometric Shapes Extended'],
    [0x1f800, 0x1f8ff, 'Supplemental Arrows-C'],
    [0x1f900, 0x1f9ff, 'Supplemental Symbols and Pictographs'],
    [0x1fa00, 0x1fa6f, 'Chess Symbols'],
    [0x1fa70, 0x1faff, 'Symbols and Pictographs Extended-A'],
    [0x1fb00, 0x1fbff, 'Symbols for Legacy Computing'],
    [0x20000, 0x2a6df, 'CJK Unified Ideographs Extension B'],
    [0x2a700, 0x2b73f, 'CJK Unified Ideographs Extension C'],
    [0x2b740, 0x2b81f, 'CJK Unified Ideographs Extension D'],
    [0x2b820, 0x2ceaf, 'CJK Unified Ideographs Extension E'],
    [0x2ceb0, 0x2ebef, 'CJK Unified Ideographs Extension F'],
    [0x2f800, 0x2fa1f, 'CJK Compatibility Ideographs Supplement'],
    [0x30000, 0x3134f, 'CJK Unified Ideographs Extension G'],
    [0xe0000, 0xe007f, 'Tags'],
    [0xe0100, 0xe01ef, 'Variation Selectors Supplement'],
    [0xf0000, 0xfffff, 'Supplementary Private Use Area-A'],
    [0x100000, 0x10ffff, 'Supplementary Private Use Area-B']
]
_block_starts = [x[0] for x in _blocks]


def get_block(c, blocks, block_starts):
    point = ord(c)
    idx = bisect.bisect_right(block_starts, point)-1
    if 0 <= idx <= len(blocks) and blocks[idx][0] <= point <= blocks[idx][1]:
        return blocks[idx]
    else:
        return -1, -1, ''


# http://yedict.com/zsts.htm
blocks_raw = """
4E00-9FA5
9FA6-9FFF
3400-4DB5
4DB6-4DBF
20000-2A6D6
2A6D7-2A6DF
2A700-2B734
2B740-2B81D
2B820-2CEA1
2CEB0-2EBE0
30000-3134A
31350-323AF
暂无unicode
2F00-2FD5
2E80-2EF3
F900-FAD9
2F800-2FA1D
31C0-31E3
2FF0-2FFB
3105-312F
31A0-31BA
"""


def get_block_han():
    block_han = []
    for l in blocks_raw.split('\n'):
        w = l.strip().split('-')
        if len(w) != 2:
            continue
        r = ["0x"+x for x in w]
        block_han.append(r)
    print(block_han)


_block_han = [[0x4E00, 0x9FA5], [0x9FA6, 0x9FFF], [0x3400, 0x4DB5], [0x4DB6, 0x4DBF], [0x20000, 0x2A6D6], [0x2A6D7, 0x2A6DF], [0x2A700, 0x2B734], [0x2B740, 0x2B81D], [0x2B820, 0x2CEA1], [
    0x2CEB0, 0x2EBE0], [0x30000, 0x3134A], [0x31350, 0x323AF], [0x2F00, 0x2FD5], [0x2E80, 0x2EF3], [0xF900, 0xFAD9], [0x2F800, 0x2FA1D], [0x31C0, 0x31E3], [0x2FF0, 0x2FFB], [0x3105, 0x312F], [0x31A0, 0x31BA]]
# block_han.sort(key=lambda x: x[0])


def is_hanzi(c):
    """
    if character c is hanzi
    """
    if c == '〇':
        return True
    point = ord(c)
    for a, b in _block_han:
        if a <= point <= b:
            return True
    return False


def is_iso_char(char):
    if is_hanzi(char):
        return True
    m, n, name = get_block(char, _blocks, _block_starts)
    if n-m+1 > 256:
        return True
    return False


def split_chars(line):
    if len(line) <= 1:
        return [line]
    tokens = []
    for x in line:
        if is_iso_char(x):
            tokens.append(' ')
            tokens.append(x)
            tokens.append(' ')
        else:
            tokens.append(x)
    w = ''.join(tokens).split()
    return [x for x in w if x]


def trunc_len(words, max_len=50, never_split=None):
    tokens = []
    for x in words:
        if not x:
            continue
        if len(x) <= max_len or (never_split and x in never_split):
            tokens.append(x)
        else:
            tokens += [x[i:i+max_len] for i in range(0, len(x), max_len)]
    return tokens

# https://www.zmonster.me/2018/10/20/nlp-road-3-unicode.html


def split_category(line):
    # if len(line) <= 1:
    # return line
    l = ''
    cat0 = cat = ''
    for x in line:
        cat = unicodedata.category(x)[0]
        if cat in 'CZ':
            x = ' '
        elif cat in 'P':
            x = ' '+x+' '
        elif cat in 'LN' and cat0 != cat:
            x = ' '+x
        cat0 = cat
        l += x
    return l


def strip_accents(line):
    line = unicodedata.normalize('NFD', line)
    l = ''
    for x in line:
        if x == '-':
            d = 0
        cat = unicodedata.category(x)
        if cat == "Mn":
            continue
        l += x
    return l


def split_lanugage(line):
    if len(line) <= 1:
        return line
    l = ''
    name0 = name = ''
    for x in line:
        try:
            name = unicodedata.name(x).split(' ')[0]
            if name != name0:
                x = ' '+x
        except:
            x = ' '
        name0 = name
        l += x
    return l


def split_punctuation(line):
    if len(line) <= 1:
        return line
    l = ''
    for x in line:
        cat = unicodedata.category(x)[0]
        if cat == "P":
            x = ' '+x+' '
        l += x
    return l


class BasicTokenizer0:
    def __init__(self, max_len=30, do_lower_case=True, never_split=None):
        self.max_len = max_len
        self.do_lower_case = do_lower_case
        self.never_split = never_split

    def tokenize(self, line):
        words = line.split()
        tokens = []
        for x in words:
            tokens += split_chars(x)
        # words = self.batch_token(split_chars, words)
        words = self.batch_token(split_category, tokens)
        if self.do_lower_case:
            for i in range(len(words)):
                if not self.never_split or words[i] not in self.never_split:
                    words[i] = words[i].lower()
            words = self.batch_token(strip_accents, words)
        words = self.batch_token(split_lanugage, words)
        words = self.batch_token(split_punctuation, words)
        words = trunc_len(words, never_split=self.never_split,
                          max_len=self.max_len)
        return words

    def batch_token(self, fn, words):
        tokens = []
        for x in words:
            if not x:
                continue
            if self.never_split and x in self.never_split:
                tokens.append(x)
            else:
                tokens += fn(x).split()
        return [x for x in tokens if x]

    def tokenize_all(self, line):
        s = line
        s = split_chars(s)
        s = split_category(s)
        if self.do_lower_case:
            s = strip_accents(s)
        s = split_lanugage(s)
        s = split_punctuation(s)
        tokens = trunc_len(
            s.split(), never_split=self.never_split, max_len=self.max_len)
        return tokens


def char_name(x):
    try:
        name = unicodedata.name(x).split(' ')[0]
    except:
        name = ""
        # raiseExceptions(f"{x} no name")

    return name


def normalize(line, do_lower_case=True, normal_type="NFD"):
    l = line.strip()
    if do_lower_case:
        l = l.lower()
    l = unicodedata.normalize(normal_type, l)
    return l


def char_split(line,split_mark=True):
    chars = []
    name0 = name = ' '
    cat0 = cat = ' '
    chars0 = [x for x in line.strip() if x]
    chars = []
    start_new_word = False
    for x in chars0:
        if start_new_word and split_mark:
            chars.append(' ')
            start_new_word = False
        cat = unicodedata.category(x)
        name = char_name(x)
        if cat[0] in 'CZ':
            chars.append(' ')
        elif cat[0] in 'PS' or is_iso_char(x):
            chars.append(' ')
            chars.append(x)
            chars.append(' ')
        elif cat[0] in 'LN':
            if cat[0] != cat0[0] or name != name0:
                chars.append(' ')
            chars.append(x)
        elif cat[0] in 'M':
            start_new_word = True
            continue
        else:
            raiseExceptions(f"{x} cat{cat} not in LMNPSZC")

        cat0 = cat
        name0 = name

    l = ''.join(chars)
    tokens = [x for x in l.split() if x]
    return tokens


class BasicTokenizer:
    def __init__(self, max_len=-1, do_lower_case=True, never_split=None):
        self.max_len = max_len
        self.do_lower_case = do_lower_case
        self.never_split = never_split

    def tokenize(self, line):
        words = line.strip().split()
        tokens = []
        for x in words:
            if self.never_split and x in self.never_split:
                tokens.append(x)
            elif not x:
                continue
            else:
                ts = char_split(x)
                
                if self.do_lower_case:
                    tsl=[]
                    for t in ts:
                        s=normalize(t)
                        us=char_split(s,split_mark=False)
                        tsl+=us
                    ts=tsl

                if self.max_len <= 0:
                    tokens += ts
                else:
                    for s in ts:
                        if len(s) <= self.max_len:
                            tokens.append(s)
                        else:
                            tokens += [s[i:i+self.max_len]
                                       for i in range(0, len(s), self.max_len)]
        return tokens


if __name__ == "__main__":
    # _read_blocks()
    # get_block_han(_blocks)
    get_block_han()
    for x in " 〇(白":
        print(is_hanzi(x))
    line = ''
    for i in range(128):
        try:
            c = chr(i)
            line += c
        except:
            pass
    line = '〇㎡[คุณจะจัดพิธีแต่งงานเมื่อไรคะัีิ์ื็ํึ]Ⅷpays-g[ran]d-blanc-élevé » (白高大夏國)'
    # s=line
    print("split_chars", split_chars(line))
    print("split_category", split_category(line))
    print("strip_accents", strip_accents(line))
    print("split_lanugage", split_lanugage(line))
    print("split_punctuation", split_punctuation(line))

    tokenizer = BasicTokenizer()
    print(tokenizer.tokenize(line))
    l2 = normalize(line)
    print(l2)
    print(char_split(line))
    print(char_split(l2))
    # for x in line:
    #     try:
    #         c = unicodedata.category(x)
    #         n = unicodedata.name(x)
    #         print(x, c, n, is_hanzi(x))
    #     except:
    #         print(x, c, 'err')
    #         pass
