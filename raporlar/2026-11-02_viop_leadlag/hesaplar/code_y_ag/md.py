def md(df, idx=True):
    d = df.reset_index() if idx else df
    cols = [str(c) for c in d.columns]
    out = ["| " + " | ".join(cols) + " |", "|" + "|".join(["---"] * len(cols)) + "|"]
    for _, r in d.iterrows():
        out.append("| " + " | ".join("" if (isinstance(v, float) and v != v) else (f"{v:.1f}" if isinstance(v, float) else str(v)) for v in r.values) + " |")
    return "\n".join(out)
