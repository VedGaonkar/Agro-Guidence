"""
translations.py — Translation helper for Agro Guidance
Uses Google Translate (via deep-translator) to convert all UI text
into the user's selected Indian language. Translations are cached
so the API is only called once per unique text+language pair.
"""

import streamlit as st

# ── Language code mapping ─────────────────────────────────────────────────────
LANG_CODES = {
    "Hindi":     "hi",
    "Marathi":   "mr",
    "Tamil":     "ta",
    "Telugu":    "te",
    "Kannada":   "kn",
    "Malayalam":  "ml",
    "Bengali":   "bn",
    "Gujarati":  "gu",
    "Punjabi":   "pa",
    "Odia":      "or",
    "Assamese":  "as",
    "Urdu":      "ur",
    "Konkani":   "gom",
    "Manipuri":  "mni-Mtei",
    "English":   "en",
}


def t(text: str) -> str:
    """
    Translate *text* into the language stored in ``st.session_state.language``.
    If the language is English (or not set), the original text is returned
    immediately without any API call.
    """
    lang = st.session_state.get("language", "English")
    lang_code = LANG_CODES.get(lang, "en")
    
    if lang_code == "en" or not text or not text.strip():
        return text

    if "t_cache" not in st.session_state:
        st.session_state.t_cache = {}

    cache_key = f"{lang_code}_{text}"
    if cache_key in st.session_state.t_cache:
        return st.session_state.t_cache[cache_key]

    try:
        from deep_translator import GoogleTranslator
        result = GoogleTranslator(source="en", target=lang_code).translate(text)
        if result and result.strip():
            st.session_state.t_cache[cache_key] = result
            return result
        return text
def t_batch(texts: list) -> list:
    """
    Translate a list of strings efficiently in a single batch.
    """
    if not texts:
        return []
        
    lang = st.session_state.get("language", "English")
    lang_code = LANG_CODES.get(lang, "en")
    
    if lang_code == "en":
        return texts

    if "t_cache" not in st.session_state:
        st.session_state.t_cache = {}

    results = []
    to_translate = []
    to_translate_indices = []

    # Check cache first
    for i, txt in enumerate(texts):
        if not txt or not txt.strip():
            results.append(txt)
            continue
            
        cache_key = f"{lang_code}_{txt}"
        if cache_key in st.session_state.t_cache:
            results.append(st.session_state.t_cache[cache_key])
        else:
            results.append(txt) # placeholder
            to_translate.append(txt)
            to_translate_indices.append(i)

    if not to_translate:
        return results

    try:
        from deep_translator import GoogleTranslator
        # GoogleTranslator allows translating batches of strings via translate_batch
        translated_batch = GoogleTranslator(source="en", target=lang_code).translate_batch(to_translate)
        
        for i, original_text, translated_text in zip(to_translate_indices, to_translate, translated_batch):
            if translated_text and translated_text.strip():
                # Update placeholder list and cache
                results[i] = translated_text
                cache_key = f"{lang_code}_{original_text}"
                st.session_state.t_cache[cache_key] = translated_text
                
        return results
    except Exception:
        # On failure, return with English fallbacks where translation failed
        return results
