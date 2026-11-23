"""Burak'ın docx'ine biçimini bozmadan paragraf/dipnot ekleme araçları.

Metin işaretleri:
  *italik*            -> italik run
  **kalın**           -> kalın run
  [[fn:ANAHTAR]]      -> dipnot referansı (dipnot metni FOOTNOTES[ANAHTAR])
"""
import copy, re, zipfile, shutil
from lxml import etree

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': W}
def q(t): return '{%s}%s' % (W, t)

TNR = ('<w:rFonts xmlns:w="%s" w:ascii="Times New Roman" w:hAnsi="Times New Roman" '
       'w:cs="Times New Roman"/>' % W)


class Doc:
    def __init__(self, path, highlight=None):
        self.path = path
        self.z = zipfile.ZipFile(path)
        self.doc = etree.fromstring(self.z.read('word/document.xml'))
        self.fn = etree.fromstring(self.z.read('word/footnotes.xml'))
        self.body = self.doc.find('w:body', NS)
        self.highlight = highlight  # ör. 'yellow' -> yeni metin vurgulu
        ids = [int(f.get(q('id'))) for f in self.fn.findall('w:footnote', NS)]
        self.next_fn = max(ids) + 1

    # ---- yardımcılar
    def paras(self):
        return [p for p in self.body.iter(q('p'))]

    def ptext(self, p):
        return ''.join(t.text or '' for t in p.iter(q('t')))

    def find_para(self, startswith, nth=0):
        hits = [p for p in self.paras() if self.ptext(p).strip().startswith(startswith)]
        if len(hits) <= nth:
            raise KeyError('paragraf yok: %r' % startswith)
        return hits[nth]

    def _rpr(self, size=24, bold=False, italic=False, hl=None, style=None, vert=None):
        r = etree.SubElement(etree.Element('x'), q('rPr'))
        if style:
            s = etree.SubElement(r, q('rStyle')); s.set(q('val'), style)
        r.append(etree.fromstring(TNR))
        if bold:
            etree.SubElement(r, q('b')); etree.SubElement(r, q('bCs'))
        if italic:
            etree.SubElement(r, q('i')); etree.SubElement(r, q('iCs'))
        sz = etree.SubElement(r, q('sz')); sz.set(q('val'), str(size))
        sz = etree.SubElement(r, q('szCs')); sz.set(q('val'), str(size))
        if hl:
            h = etree.SubElement(r, q('highlight')); h.set(q('val'), hl)
        if vert:
            v = etree.SubElement(r, q('vertAlign')); v.set(q('val'), vert)
        return r

    def _run(self, text, size=24, bold=False, italic=False, hl=None):
        r = etree.Element(q('r'))
        r.append(self._rpr(size, bold, italic, hl))
        t = etree.SubElement(r, q('t')); t.text = text
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
        return r

    def _fnref_run(self, fid, hl=None):
        r = etree.Element(q('r'))
        r.append(self._rpr(24, style='DipnotBavurusu', hl=hl))
        f = etree.SubElement(r, q('footnoteReference')); f.set(q('id'), str(fid))
        return r

    def _runs_from_markup(self, text, size=24, hl=None, footnotes=None, base_bold=False):
        """{+eklenen+} -> sarı, {~düzeltilen~} -> turkuaz (yalnız self.highlight açıksa)."""
        out = []
        for seg in re.split(r'(\{\+.*?\+\}|\{~.*?~\})', text, flags=re.S):
            if not seg:
                continue
            seg_hl = hl
            if seg.startswith('{+'):
                seg, seg_hl = seg[2:-2], ('yellow' if self.highlight else None)
            elif seg.startswith('{~'):
                seg, seg_hl = seg[2:-2], ('cyan' if self.highlight else None)
            out.extend(self._runs_plain(seg, size, seg_hl, footnotes, base_bold))
        return out

    def _runs_plain(self, text, size=24, hl=None, footnotes=None, base_bold=False):
        out = []
        for tok in re.split(r'(\[\[fn:.*?\]\]|\*\*[^*]+\*\*|\*[^*]+\*)', text, flags=re.S):
            if not tok:
                continue
            m = re.match(r'\[\[fn:(.*?)\]\]$', tok, flags=re.S)
            if m:
                key = m.group(1)
                fn_text = footnotes[key] if footnotes and key in footnotes else key
                fn_hl = 'green' if (self.highlight and fn_text.startswith('BCA')) else None
                fid = self.add_footnote(fn_text, hl=fn_hl)
                out.append(self._fnref_run(fid))
            elif tok.startswith('**'):
                out.append(self._run(tok[2:-2], size, True, False, hl))
            elif tok.startswith('*'):
                out.append(self._run(tok[1:-1], size, base_bold, True, hl))
            else:
                out.append(self._run(tok, size, base_bold, False, hl))
        return out

    # ---- dipnot
    def add_footnote(self, text, hl=None):
        fid = self.next_fn; self.next_fn += 1
        f = etree.SubElement(self.fn, q('footnote')); f.set(q('id'), str(fid))
        self._fill_footnote(f, text, hl)
        return fid

    def _fill_footnote(self, f, text, hl=None):
        for c in list(f):
            f.remove(c)
        p = etree.SubElement(f, q('p'))
        ppr = etree.SubElement(p, q('pPr'))
        sp = etree.SubElement(ppr, q('spacing')); sp.set(q('after'), '0'); sp.set(q('line'), '240'); sp.set(q('lineRule'), 'auto')
        jc = etree.SubElement(ppr, q('jc')); jc.set(q('val'), 'both')
        r = etree.SubElement(p, q('r'))
        r.append(self._rpr(20, style='DipnotBavurusu', hl=hl))
        etree.SubElement(r, q('footnoteRef'))
        p.append(self._run(' ', 20, hl=hl))
        for run in self._runs_plain(text, size=20, hl=hl):
            p.append(run)

    def set_footnote(self, fid, text, hl=None):
        for f in self.fn.findall('w:footnote', NS):
            if f.get(q('id')) == str(fid):
                self._fill_footnote(f, text, hl)
                return
        raise KeyError(fid)

    # ---- paragraf ekleme
    def new_para(self, text, footnotes=None, kind='body', hl=None):
        """kind: body | heading | center_bold | bib"""
        p = etree.Element(q('p'))
        ppr = etree.SubElement(p, q('pPr'))
        sp = etree.SubElement(ppr, q('spacing'))
        if kind == 'bib':
            sp.set(q('line'), '360'); sp.set(q('lineRule'), 'auto')
            ind = etree.SubElement(ppr, q('ind')); ind.set(q('left'), '709'); ind.set(q('hanging'), '709')
        else:
            sp.set(q('after'), '200'); sp.set(q('line'), '360'); sp.set(q('lineRule'), 'auto')
        jc = etree.SubElement(ppr, q('jc'))
        jc.set(q('val'), 'center' if kind == 'center_bold' else 'both')
        if kind == 'body':
            ind = etree.SubElement(ppr, q('ind')); ind.set(q('firstLine'), '709')
        bold = kind in ('heading', 'center_bold')
        for run in self._runs_from_markup(text, 24, hl, footnotes, base_bold=bold):
            p.append(run)
        return p

    def insert_after(self, anchor, paras):
        for p in paras:
            anchor.addnext(p)
            anchor = p
        return anchor

    def insert_before(self, anchor, paras):
        for p in paras:
            anchor.addprevious(p)

    # ---- mevcut paragrafta işlem
    def replace_in_para(self, p, old, new):
        """Tek bir w:t içinde geçen metni değiştirir; geçmezse paragrafı birleştirip dener."""
        for t in p.iter(q('t')):
            if t.text and old in t.text:
                t.text = t.text.replace(old, new, 1)
                return True
        # w:t'ler arasında bölünmüşse: ilgili t'leri birleştir
        ts = [t for t in p.iter(q('t'))]
        full = ''.join(t.text or '' for t in ts)
        i = full.find(old)
        if i < 0:
            raise KeyError('metin yok: %r' % old)
        j = i + len(old)
        pos = 0; first = True
        for t in ts:
            txt = t.text or ''
            s, e = pos, pos + len(txt)
            if e > i and s < j:
                if first:
                    t.text = txt[:i - s] + new + (txt[j - s:] if j < e else '')
                    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
                    first = False
                else:
                    t.text = txt[j - s:] if j < e else ''
            pos = e
        return True

    def add_fnref_after(self, p, anchor_text, fn_text, hl=None):
        """anchor_text'in bittiği yere dipnot referansı koyar (run'u böler)."""
        for r in p.findall('w:r', NS):
            t = r.find('w:t', NS)
            if t is None or not t.text or anchor_text not in t.text:
                continue
            k = t.text.index(anchor_text) + len(anchor_text)
            before, after = t.text[:k], t.text[k:]
            t.text = before
            t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
            fid = self.add_footnote(fn_text, hl=hl)
            ref = self._fnref_run(fid, hl=hl)
            r.addnext(ref)
            if after:
                r2 = copy.deepcopy(r)
                r2.find('w:t', NS).text = after
                ref.addnext(r2)
            return fid
        raise KeyError('çapa yok: %r' % anchor_text)

    def append_text(self, p, text, footnotes=None, hl=None):
        for run in self._runs_from_markup(text, 24, hl, footnotes):
            p.append(run)

    def remove(self, p):
        p.getparent().remove(p)

    def rebuild(self, p, markup, bold=False, size=24):
        """Paragrafın pPr'sini koruyup içeriğini markup ile yeniden yazar."""
        for c in list(p):
            if c.tag != q('pPr'):
                p.remove(c)
        for run in self._runs_from_markup(markup, size, None, None, base_bold=bold):
            p.append(run)
        return p

    def para_like(self, template, markup, bold=False, size=24, hanging=False, spacing=None):
        p = etree.Element(q('p'))
        tp = template.find('w:pPr', NS)
        if tp is not None:
            ppr = copy.deepcopy(tp)
            for c in list(ppr):
                if c.tag in (q('numPr'), q('pStyle')):
                    ppr.remove(c)
            if hanging:
                for c in ppr.findall('w:ind', NS):
                    ppr.remove(c)
                ind = etree.Element(q('ind')); ind.set(q('left'), '709'); ind.set(q('hanging'), '709')
                jc = ppr.find('w:jc', NS)
                (jc.addprevious(ind) if jc is not None else ppr.append(ind))
            if spacing is not None:
                for c in ppr.findall('w:spacing', NS):
                    ppr.remove(c)
                sp = etree.Element(q('spacing'))
                for k, v in spacing.items():
                    sp.set(q(k), v)
                ppr.insert(0, sp)
            p.append(ppr)
        for run in self._runs_from_markup(markup, size, None, None, base_bold=bold):
            p.append(run)
        return p

    def prune_footnotes(self):
        used = {r.get(q('id')) for r in self.doc.iter(q('footnoteReference'))}
        for f in self.fn.findall('w:footnote', NS):
            fid = f.get(q('id'))
            if int(fid) > 0 and fid not in used:
                self.fn.remove(f)

    # ---- kaydet
    def save(self, out):
        tmp = out + '.tmp'
        with zipfile.ZipFile(self.path) as zin, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == 'word/document.xml':
                    data = etree.tostring(self.doc, xml_declaration=True, encoding='UTF-8', standalone=True)
                elif item.filename == 'word/footnotes.xml':
                    data = etree.tostring(self.fn, xml_declaration=True, encoding='UTF-8', standalone=True)
                zout.writestr(item, data)
        shutil.move(tmp, out)
