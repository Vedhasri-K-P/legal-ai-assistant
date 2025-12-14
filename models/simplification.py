"""
Legal jargon simplification model for 10-year-old reading level
"""
import os
import re
import json
from config.config import SIMPLIFICATION_MODEL, DICTIONARIES_DIR

def load_legal_terms():
    """Load legal terms dictionary from JSON file"""
    legal_terms_path = os.path.join(DICTIONARIES_DIR, "legal_terms.json")
    
    # Create default legal terms if file doesn't exist
    if not os.path.exists(legal_terms_path):
        default_legal_terms = {
            "hereinafter": "from now on",
            "aforementioned": "mentioned earlier",
            "pursuant to": "according to",
            "notwithstanding": "even though",
            "hereby": "by this",
            "therein": "in that",
            "forthwith": "right away",
            "whereas": "because",
            "shall": "will",
            "null and void": "not valid",
            "without prejudice": "without losing rights",
            "in witness whereof": "as proof",
            "witnesseth": "shows",
            "in perpetuity": "forever",
            "heretofore": "before now",
            "hereto": "to this",
            "herewith": "with this",
            "herein": "in here",
            "hereunder": "below",
            "hereunto": "to this",
            "thereunto": "to that",
            "thereby": "by that",
            "thereafter": "after that",
            "thereof": "of that",
            "thereto": "to that",
            "whatsoever": "at all",
            "whomsoever": "anyone",
            "whosoever": "whoever",
            "wherein": "where",
            "whereof": "of which",
            "whereby": "by which",
            "prima facie": "at first look",
            "mutatis mutandis": "with necessary changes",
            "inter alia": "among other things",
            "bona fide": "genuine",
            "status quo": "current state",
            "de facto": "in fact",
            "de jure": "by law",
            "per se": "by itself",
            "viz.": "namely",
            "i.e.": "that is",
            "e.g.": "for example",
            "et al.": "and others",
            "ibid.": "in the same place",
            "supra": "above",
            "infra": "below",
            "ante": "before",
            "post": "after",
            "force majeure": "unexpected event",
            "quantum meruit": "reasonable payment",
            "estoppel": "can't deny",
            "injunction": "court order",
            "tort": "harm",
            "lien": "legal claim",
            "enjoin": "order",
            "stipulate": "state clearly",
            "covenant": "promise",
            "indemnify": "protect from loss",
            "jurisdiction": "authority",
            "consideration": "payment or exchange",
            "waiver": "giving up rights",
            "ipso facto": "by that fact",
            "quid pro quo": "something for something",
            "ultra vires": "beyond power",
            "subject to": "depending on",
            "ab initio": "from the start",
            "in lieu of": "instead of",
            "in re": "regarding",
            "in situ": "in its original place",
            "in toto": "completely",
            "in personam": "against a person",
            "in rem": "against a thing",
            "sui generis": "unique",
            "caveat emptor": "buyer beware",
            "pro rata": "proportionally",
            "sine qua non": "essential part",
            "res ipsa loquitur": "the thing speaks for itself",
            "pro bono": "for free",
            "ex parte": "from one side only",
            "modus operandi": "way of doing things",
            "per curiam": "by the court",
            "sub judice": "under judgment",
            "amicus curiae": "friend of the court",
            "obiter dictum": "side remark",
            "habeas corpus": "produce the body",
            "stare decisis": "stand by decided cases",
            "corpus delicti": "body of the crime",
            "mens rea": "guilty mind",
            "actus reus": "guilty act",
            "mala in se": "wrong in itself",
            "mala prohibita": "wrong because prohibited",
            "subpoena": "court order",
            "affidavit": "written statement",
            "deposition": "testimony",
            "interrogatory": "written question",
            "statute of limitations": "time limit",
            "venue": "location",
            "voir dire": "jury selection",
            "liquidated damages": "agreed payment for breach",
            "specific performance": "court-ordered fulfillment",
            "res judicata": "already decided"
        }
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(legal_terms_path), exist_ok=True)
        
        # Save default legal terms
        with open(legal_terms_path, 'w') as f:
            json.dump(default_legal_terms, f, indent=2)
        
        return default_legal_terms
    
    # Load legal terms from file
    try:
        with open(legal_terms_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading legal terms: {e}")
        return {}

def simplify_legal_jargon(text: str) -> str:
    """
    Simplify legal jargon to very simple language suitable for a 10-year-old
    
    Args:
        text: Legal text to simplify
        
    Returns:
        Simplified text
    """
    # Load legal terms dictionary
    legal_terms = load_legal_terms()
    
    # Step 1: Replace legal terms with simpler equivalents
    simplified_text = text
    for term, simple_term in legal_terms.items():
        # Create a regex pattern that matches the term as a whole word
        pattern = r'\b' + re.escape(term) + r'\b'
        simplified_text = re.sub(pattern, simple_term, simplified_text, flags=re.IGNORECASE)
    
    # Step 2: Custom replacements for common legal phrases
    phrase_replacements = {
        r"party of the first part": "the first person",
        r"party of the second part": "the second person",
        r"for the avoidance of doubt": "to be clear",
        r"for all intents and purposes": "in every way",
        r"in the event that": "if",
        r"in the absence of": "without",
        r"at the sole discretion of": "chosen only by",
        r"in accordance with": "following",
        r"with reference to": "about",
        r"with respect to": "about",
        r"with regard to": "about",
        r"for the purpose of": "to",
        r"prior to": "before",
        r"subsequent to": "after",
        r"in excess of": "more than",
        r"in connection with": "related to",
        r"in relation to": "about",
        r"in the course of": "during",
        r"on the basis of": "because of",
        r"on the grounds that": "because",
        r"by virtue of": "because of",
        r"in light of": "because of",
        r"for the benefit of": "for",
        r"for and on behalf of": "for",
        r"from time to time": "sometimes",
        r"as the case may be": "as needed",
        r"set forth": "written",
        r"cease and desist": "stop",
        r"acknowledged and agreed": "accepted",
        r"represents and warrants": "promises",
        r"terms and conditions": "rules",
        r"bind and inure": "apply",
        r"force and effect": "power",
        r"indemnify and hold harmless": "protect",
        r"due and payable": "owed",
        r"execute and deliver": "sign",
        r"assign and transfer": "give",
        r"rights and remedies": "options",
        r"right, title and interest": "ownership",
        r"covenants and agreements": "promises",
        r"successors and assigns": "future owners"
    }
    
    for phrase, replacement in phrase_replacements.items():
        simplified_text = re.sub(phrase, replacement, simplified_text, flags=re.IGNORECASE)
    
    # Step 3: Function to break long sentences into shorter ones
    def break_long_sentences(text):
        sentences = re.split(r'(?<=[.!?])\s+', text)
        simplified_sentences = []
        
        for sentence in sentences:
            # If sentence is very long, try to split it
            if len(sentence.split()) > 15:  # Lowered threshold for kid-friendly reading
                # Try to split on semicolons, commas, and other natural break points
                parts = re.split(r';|, (?:and|but|or|however|therefore|nevertheless|furthermore|moreover|thus|consequently)', sentence)
                for part in parts:
                    if part.strip():
                        # Add period if not already there
                        if not part.strip().endswith(('.', '!', '?')):
                            part += '.'
                        simplified_sentences.append(part.strip())
            else:
                simplified_sentences.append(sentence)
        
        return ' '.join(simplified_sentences)
    
    # Apply sentence breaking
    simplified_text = break_long_sentences(simplified_text)
    
    # Step 4: Further kid-friendly modifications
    
    # Replace complex legal words with kid-friendly equivalents
    kid_friendly_terms = {
        r"\bagree(?:s|d|ment)?\b": "promise",
        r"\bcontract(?:s|ual)?\b": "deal",
        r"\b(?:shall|must|obligated to)\b": "need to",
        r"\bobligations?\b": "duties",
        r"\bliable\b": "responsible",
        r"\bliability\b": "responsibility",
        r"\bexecute\b": "sign",
        r"\bterminate\b": "end",
        r"\bprovision(?:s)?\b": "rule",
        r"\benter into\b": "make",
        r"\bcompensation\b": "payment",
        r"\bremuneration\b": "money",
        r"\bdeemed\b": "considered",
        r"\bauthorized\b": "allowed",
        r"\bprohibited\b": "not allowed",
        r"\bpermitted\b": "allowed",
        r"\bcompliance\b": "following the rules",
        r"\bviolation\b": "breaking the rules",
        r"\bconstitute\b": "be",
        r"\bconsideration\b": "payment",
        r"\bprocure\b": "get",
        r"\butilize\b": "use",
        r"\b(?:require|necessitate)(?:s|d)?\b": "need",
        r"\bcommence(?:s|d|ment)?\b": "start",
        r"\bproceed(?:s|ed|ing)?\b": "go ahead",
        r"\bfurnish(?:es|ed)?\b": "give",
        r"\bwitness(?:es|ed)?\b": "see",
        r"\bascertain\b": "find out",
        r"\b(?:advise|notify)(?:s|d|ing)?\b": "tell",
        r"\btransmit(?:s|ted)?\b": "send",
        r"\bpurchase(?:s|d)?\b": "buy",
        r"\btransfer(?:s|red)?\b": "move",
        r"\bconvey(?:s|ed|ance)?\b": "give",
        r"\brelinquish(?:es|ed)?\b": "give up",
        r"\bdocument(?:s|ation)?\b": "paper",
        r"\bstatement(?:s)?\b": "message",
        r"\brepresent(?:s|ed|ations)?\b": "say",
        r"\bwarrant(?:s|ed|y|ies)?\b": "promise",
        r"\bendeavor\b": "try",
        r"\battempt\b": "try",
        r"\bundertake\b": "try",
        r"\bfabricate\b": "make",
        r"\bconstruct\b": "build",
        r"\bmanufacture\b": "make",
        r"\bcompel(?:s|led)?\b": "force",
        r"\bobligation\b": "duty",
        r"\bmandatory\b": "required",
        r"\bvoluntary\b": "optional",
        r"\bincorporate(?:s|d)?\b": "include",
        r"\binherent\b": "built-in",
        r"\bhereby\b": "by this",
        r"\bthus\b": "so",
        r"\bclaim(?:s|ed)?\b": "ask for",
        r"\brequest(?:s|ed)?\b": "ask for",
        r"\bdemand(?:s|ed)?\b": "ask for",
        r"\binvoice(?:s|d)?\b": "bill",
        r"\bauthorization\b": "permission",
        r"\bconsent\b": "agreement",
        r"\bapproval\b": "okay",
        r"\bendorsement\b": "support",
        r"\bthe undersigned\b": "I",
        r"\bsignatory\b": "person who signs",
        r"\bcounterparty\b": "other person",
        r"\badhere to\b": "follow",
        r"\bcomply with\b": "follow",
        r"\bcommensurate with\b": "matching",
        r"\bdispute(?:s|d)?\b": "disagreement",
        r"\bconflict(?:s|ing)?\b": "disagreement",
        r"\bregulation(?:s)?\b": "rule",
        r"\bamendment(?:s)?\b": "change",
        r"\bcommodity\b": "thing",
        r"\bperiodically\b": "sometimes",
        r"\bsubsequently\b": "later",
        r"\bprior to\b": "before",
        r"\bhereafter\b": "from now on",
        r"\bhereinafter\b": "from now on",
        r"\bheretofore\b": "until now",
        r"\bthe parties\b": "the people",
        r"\baforesaid\b": "already mentioned",
        r"\bsupersede(?:s|d)?\b": "replace",
        r"\bprecludes?\b": "prevent",
        r"\bprohibits?\b": "not allow",
        r"\brestricts?\b": "limit",
        r"\brequires?\b": "need",
        r"\bforthwith\b": "right away",
        r"\bexpeditious(?:ly)?\b": "quickly",
        r"\bexempt(?:ed|ion)?\b": "not included",
        r"\badditional\b": "extra",
        r"\bdeficient\b": "not enough",
        r"\bexcessive\b": "too much",
        r"\binclude, but not limited to\b": "include",
        r"\bincluding, without limitation\b": "including"
    }
    
    for term, replacement in kid_friendly_terms.items():
        simplified_text = re.sub(term, replacement, simplified_text, flags=re.IGNORECASE)
    
    # Replace "Committee" and "Contractor" with simpler terms
    simplified_text = simplified_text.replace("the Committee", "Person A")
    simplified_text = simplified_text.replace("the Contractor", "Person B")
    
    # Simplify complex sentence structures 
    simplified_text = simplified_text.replace("Subject to the terms and conditions", "Following the rules")
    simplified_text = simplified_text.replace("as set forth", "written")
    simplified_text = simplified_text.replace("as an independent contractor", "as a worker")
    simplified_text = simplified_text.replace("independent contractor", "worker")
    simplified_text = simplified_text.replace("hereby", "")  # Often unnecessary
    simplified_text = simplified_text.replace("shall be", "is")
    simplified_text = simplified_text.replace("shall", "will")
    simplified_text = simplified_text.replace("may be amended", "can be changed")
    simplified_text = simplified_text.replace("supplemented with", "added to with")
    simplified_text = simplified_text.replace("rendered by", "done by")
    simplified_text = simplified_text.replace("collectively are", "are all")
    simplified_text = simplified_text.replace("incorporated by reference", "included")
    
    # Make sentences active rather than passive where possible
    simplified_text = re.sub(r"is ([\w]+)ed by", r"\1s", simplified_text)
    simplified_text = re.sub(r"are ([\w]+)ed by", r"\1", simplified_text)
    
    # Step 5: Final readability improvements
    
    # Replace long numbers with words
    number_words = {
        "1": "one", "2": "two", "3": "three", "4": "four", "5": "five",
        "6": "six", "7": "seven", "8": "eight", "9": "nine", "10": "ten"
    }
    for num, word in number_words.items():
        simplified_text = re.sub(r'\b' + num + r'\b', word, simplified_text)
    
    # Remove complex punctuation
    simplified_text = simplified_text.replace(";", ".")
    simplified_text = simplified_text.replace(":", ".")
    
    # Fix any double periods
    simplified_text = simplified_text.replace("..", ".")
    
    # Add space after periods if missing
    simplified_text = re.sub(r'\.([A-Z])', r'. \1', simplified_text)
    
    # Ensure proper spacing
    simplified_text = re.sub(r'\s+', ' ', simplified_text)
    
    return simplified_text