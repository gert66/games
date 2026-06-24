import streamlit as st
import random
import time

# ─── Configuratie ────────────────────────────────────────────────────────────

DIEREN = [
    ("🐶", "Hond"),
    ("🐱", "Kat"),
    ("🐼", "Panda"),
    ("🐘", "Olifant"),
    ("🦁", "Leeuw"),
    ("🐯", "Tijger"),
    ("🐰", "Konijn"),
    ("🐴", "Paard"),
    ("🐬", "Dolfijn"),
    ("🐧", "Pinguïn"),
    ("🐢", "Schildpad"),
    ("🦊", "Vos"),
    ("🦉", "Uil"),
    ("🦔", "Egel"),
    ("🦒", "Giraffe"),
    ("🦓", "Zebra"),
    ("🐸", "Kikker"),
    ("🦋", "Vlinder"),
    ("🐙", "Octopus"),
    ("🦈", "Haai"),
    ("🦚", "Pauw"),
    ("🦜", "Papegaai"),
    ("🐊", "Krokodil"),
    ("🦦", "Otter"),
    ("🐺", "Wolf"),
    ("🐻", "Beer"),
    ("🦝", "Wasbeer"),
    ("🦙", "Lama"),
    ("🐿️", "Eekhoorn"),
    ("🦩", "Flamingo"),
    ("🐠", "Tropische vis"),
    ("🦌", "Hert"),
]

KAART_ACHTERKANT = "❓"
ROOSTER_KOLOMMEN = 8

# ─── Spel initialisatie ───────────────────────────────────────────────────────

def nieuw_spel():
    """Maak een nieuw speldeck aan en reset alle spelstatus."""
    deck = []
    for idx, (emoji, naam) in enumerate(DIEREN):
        # Elke dier verschijnt twee keer (een paar)
        deck.append({"id": idx * 2,     "dier_id": idx, "emoji": emoji, "naam": naam, "open": False, "gevonden": False})
        deck.append({"id": idx * 2 + 1, "dier_id": idx, "emoji": emoji, "naam": naam, "open": False, "gevonden": False})
    random.shuffle(deck)

    st.session_state.deck = deck
    st.session_state.open_kaarten = []      # maximaal 2 kaarten tegelijk open
    st.session_state.speler = 1             # huidige speler (1 of 2)
    st.session_state.scores = {1: 0, 2: 0}
    st.session_state.bericht = ""           # feedback bericht voor de speler
    st.session_state.spelklaar = False      # True als alle paren gevonden zijn
    st.session_state.wacht_op_reset = False # True terwijl we wachten voor ongelijk paar

def init_staat():
    """Initialiseer session_state als het spel nog niet gestart is."""
    if "deck" not in st.session_state:
        nieuw_spel()

# ─── Spellogica ───────────────────────────────────────────────────────────────

def kaart_klik(kaart_idx: int):
    """Verwerk een klik op kaart met index kaart_idx in het deck."""
    if st.session_state.spelklaar:
        return

    # Blokkeer klikken als we een ongelijk paar tonen (reset staat)
    if st.session_state.wacht_op_reset:
        # Reset het ongelijke paar
        for k in st.session_state.deck:
            if k["open"] and not k["gevonden"]:
                k["open"] = False
        st.session_state.open_kaarten = []
        st.session_state.wacht_op_reset = False
        st.session_state.bericht = f"🎮 Speler {st.session_state.speler} is aan de beurt"
        return

    kaart = st.session_state.deck[kaart_idx]

    # Negeer klik op al open of gevonden kaart
    if kaart["open"] or kaart["gevonden"]:
        return

    # Negeer als er al 2 kaarten open zijn
    if len(st.session_state.open_kaarten) >= 2:
        return

    # Zet kaart open
    kaart["open"] = True
    st.session_state.open_kaarten.append(kaart_idx)

    # Controleer of er twee kaarten open zijn
    if len(st.session_state.open_kaarten) == 2:
        idx_a, idx_b = st.session_state.open_kaarten
        kaart_a = st.session_state.deck[idx_a]
        kaart_b = st.session_state.deck[idx_b]

        if kaart_a["dier_id"] == kaart_b["dier_id"]:
            # Paar gevonden!
            kaart_a["gevonden"] = True
            kaart_b["gevonden"] = True
            st.session_state.scores[st.session_state.speler] += 1
            st.session_state.open_kaarten = []
            st.session_state.bericht = (
                f"✅ Speler {st.session_state.speler} vond een paar: "
                f"{kaart_a['emoji']} {kaart_a['naam']}! Nog een keer!"
            )

            # Controleer of het spel klaar is
            if all(k["gevonden"] for k in st.session_state.deck):
                st.session_state.spelklaar = True
        else:
            # Geen paar — wissel speler, kaarten blijven zichtbaar tot volgende klik
            volgende = 2 if st.session_state.speler == 1 else 1
            st.session_state.bericht = (
                f"❌ Geen paar ({kaart_a['emoji']} + {kaart_b['emoji']}). "
                f"Speler {volgende} is aan de beurt. Klik ergens om door te gaan."
            )
            st.session_state.speler = volgende
            st.session_state.wacht_op_reset = True

# ─── Stijl ───────────────────────────────────────────────────────────────────

def laad_css():
    st.markdown(
        """
        <style>
        /* Algemene achtergrond */
        .stApp {
            background: linear-gradient(135deg, #e0f7fa 0%, #b2ebf2 50%, #e8f5e9 100%);
        }

        /* Titel stijl */
        .titel {
            text-align: center;
            font-size: 3em;
            font-weight: 900;
            color: #1a237e;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.2);
            margin-bottom: 0.2em;
        }

        /* Score paneel */
        .score-balk {
            display: flex;
            justify-content: center;
            gap: 2em;
            margin: 0.5em 0;
        }
        .score-box {
            background: white;
            border-radius: 16px;
            padding: 0.6em 1.4em;
            font-size: 1.15em;
            font-weight: 700;
            box-shadow: 0 4px 12px rgba(0,0,0,0.12);
            border: 3px solid #90caf9;
        }
        .score-box.actief {
            border-color: #f57c00;
            background: #fff3e0;
            transform: scale(1.05);
        }

        /* Beurt bericht */
        .bericht {
            text-align: center;
            font-size: 1.1em;
            font-weight: 600;
            color: #4a148c;
            background: rgba(255,255,255,0.85);
            border-radius: 12px;
            padding: 0.5em 1em;
            margin: 0.4em auto;
            max-width: 600px;
        }

        /* Kaart knop stijl — overschrijf Streamlit defaults */
        div[data-testid="stButton"] button {
            width: 100% !important;
            height: 86px !important;
            font-size: 3em !important;       /* groot genoeg voor duidelijke emoji's */
            border-radius: 12px !important;
            border: none !important;
            cursor: pointer !important;
            transition: transform 0.15s, box-shadow 0.15s !important;
            padding: 0 !important;
            line-height: 86px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }

        /* Dichte kaart */
        div[data-testid="stButton"] button[kind="secondary"] {
            background: linear-gradient(145deg, #1565c0, #1e88e5) !important;
            color: white !important;
            font-size: 2.6em !important;     /* vraagteken iets kleiner dan dier-emoji */
            box-shadow: 0 4px 10px rgba(21,101,192,0.4) !important;
        }
        div[data-testid="stButton"] button[kind="secondary"]:hover {
            transform: scale(1.08) !important;
            box-shadow: 0 6px 16px rgba(21,101,192,0.5) !important;
        }

        /* Open / gevonden kaart */
        div[data-testid="stButton"] button[kind="primary"] {
            background: linear-gradient(145deg, #ffffff, #f1f8e9) !important;
            color: #1b5e20 !important;
            box-shadow: 0 2px 6px rgba(0,0,0,0.15) !important;
        }

        /* Verberg de kolom-padding zodat het rooster dicht op elkaar staat */
        div[data-testid="column"] {
            padding: 2px !important;
        }

        /* Einde spel banner */
        .einde-banner {
            text-align: center;
            font-size: 2em;
            font-weight: 900;
            color: #b71c1c;
            background: #fff9c4;
            border-radius: 20px;
            padding: 0.6em 1em;
            margin: 0.5em auto;
            max-width: 700px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# ─── UI ──────────────────────────────────────────────────────────────────────

def toon_header():
    """Toon titel, scores en statusbericht."""
    st.markdown('<div class="titel">🐾 Dieren Memory 🐾</div>', unsafe_allow_html=True)

    s1_class = "score-box actief" if st.session_state.speler == 1 else "score-box"
    s2_class = "score-box actief" if st.session_state.speler == 2 else "score-box"
    scores = st.session_state.scores

    st.markdown(
        f"""
        <div class="score-balk">
            <div class="{s1_class}">🧒 Speler 1: {scores[1]} paar{'s' if scores[1] != 1 else ''}</div>
            <div class="{s2_class}">👧 Speler 2: {scores[2]} paar{'s' if scores[2] != 1 else ''}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.bericht:
        st.markdown(
            f'<div class="bericht">{st.session_state.bericht}</div>',
            unsafe_allow_html=True,
        )


def toon_einde():
    """Toon winnaar en ballonnen als het spel klaar is."""
    s1 = st.session_state.scores[1]
    s2 = st.session_state.scores[2]

    if s1 > s2:
        tekst = f"🏆 Speler 1 wint met {s1} paren! Geweldig! 🎉"
    elif s2 > s1:
        tekst = f"🏆 Speler 2 wint met {s2} paren! Geweldig! 🎉"
    else:
        tekst = f"🤝 Gelijkspel! Allebei {s1} paren. Super gespeeld! 🌟"

    st.markdown(f'<div class="einde-banner">{tekst}</div>', unsafe_allow_html=True)
    st.balloons()


def toon_rooster():
    """Teken het 8x8 rooster van kaarten."""
    deck = st.session_state.deck

    for rij in range(8):
        kolommen = st.columns(ROOSTER_KOLOMMEN, gap="small")
        for kolom in range(ROOSTER_KOLOMMEN):
            kaart_idx = rij * ROOSTER_KOLOMMEN + kolom
            kaart = deck[kaart_idx]

            with kolommen[kolom]:
                if kaart["gevonden"]:
                    # Gevonden kaart — toon emoji, niet klikbaar
                    st.button(
                        kaart["emoji"],
                        key=f"k_{kaart['id']}",
                        use_container_width=True,
                        type="primary",
                        disabled=True,
                    )
                elif kaart["open"]:
                    # Omgedraaide kaart — toon emoji, klik = reset ongelijk paar
                    if st.button(
                        kaart["emoji"],
                        key=f"k_{kaart['id']}",
                        use_container_width=True,
                        type="primary",
                    ):
                        kaart_klik(kaart_idx)
                        st.rerun()
                else:
                    # Dichte kaart
                    if st.button(
                        KAART_ACHTERKANT,
                        key=f"k_{kaart['id']}",
                        use_container_width=True,
                        type="secondary",
                    ):
                        kaart_klik(kaart_idx)
                        st.rerun()


def toon_spelregels():
    """Uitklapbaar blok met spelregels."""
    with st.expander("📖 Spelregels"):
        st.markdown(
            """
            **Hoe speel je Dieren Memory?**

            1. Alle 64 kaarten liggen omgekeerd op tafel.
            2. Speler 1 begint en klikt twee kaarten open.
            3. **Paar gevonden?** ✅
               De kaarten blijven open en je mag **nog een keer**!
            4. **Geen paar?** ❌
               Klik ergens om de kaarten terug te draaien. De andere speler is aan de beurt.
            5. Het spel is klaar als alle 32 paren gevonden zijn.
            6. De speler met de meeste paren **wint**!

            *Tip: onthoud goed waar welk dier zit!* 🧠
            """
        )

# ─── Hoofdprogramma ───────────────────────────────────────────────────────────

def main():
    st.set_page_config(
        page_title="Dieren Memory",
        page_icon="🐾",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    laad_css()
    init_staat()

    toon_header()

    # Nieuw spel knop
    col_midden = st.columns([3, 1, 3])[1]
    with col_midden:
        if st.button("🔄 Nieuw spel", use_container_width=True):
            nieuw_spel()
            st.rerun()

    st.markdown("---")

    # Einde banner
    if st.session_state.spelklaar:
        toon_einde()

    # Kaarten rooster
    toon_rooster()

    st.markdown("---")
    toon_spelregels()


if __name__ == "__main__":
    main()
