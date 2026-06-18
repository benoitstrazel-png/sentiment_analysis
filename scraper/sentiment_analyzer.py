import re

class SentimentAnalyzer:
    def __init__(self):
        # A list of common positive and negative words in French
        self.french_positive = {
            "excellent", "super", "génial", "top", "magnifique", "parfait", "adore", "adoré", "ravis", 
            "ravie", "très bon", "très bien", "superbe", "incroyable", "rapide", "efficace", "facile", 
            "fluide", "géniale", "satisfait", "satisfaite", "merveilleux", "recommande", "réussi", 
            "extraordinaire", "qualité", "meilleur", "amour", "géniaux", "parfaite", "parfaits", "top"
        }
        
        self.french_negative = {
            "mauvais", "nul", "déçu", "déçue", "décevant", "problème", "problèmes", "panne", "casse", 
            "lent", "lenteur", "bug", "bugs", "erreur", "erreurs", "pire", "horrible", "regret", 
            "regrette", "dommage", "cher", "chère", "inutile", "mécontent", "mécontente", "faible", 
            "insuffisant", "défaut", "défauts", "compliqué", "difficile", "nul", "nulle", "lourd"
        }
        
        self.english_positive = {
            "excellent", "great", "awesome", "perfect", "love", "loved", "amazing", "good", "nice", 
            "best", "fast", "easy", "satisfied", "wonderful", "recommend", "beautiful", "smooth"
        }
        
        self.english_negative = {
            "bad", "disappointed", "disappointing", "issue", "issues", "problem", "problems", "slow", 
            "bug", "bugs", "error", "worst", "horrible", "regret", "expensive", "useless", "weak", 
            "defect", "difficult", "heavy", "terrible", "poor", "waste"
        }

        # Aspects Mapping by Category
        self.ASPECTS_MAP = {
            "watch": {
                "confort": ["confort", "confortable", "bracelet", "poignet", "léger", "poids", "agréable"],
                "ecran": ["écran", "ecran", "luminosité", "lumineux", "affichage", "tactile", "verre"],
                "applications": ["application", "appli", "applis", "applications", "santé", "sommeil", "cardiaque", "tension", "ecg", "suivi", "gps", "mesures", "sport"],
                "batterie": ["batterie", "autonomie", "charge", "charger", "tient", "jours", "heures", "pile"]
            },
            "buds": {
                "confort": ["confort", "confortable", "maintien", "oreille", "oreilles", "tient", "glisse", "léger"],
                "audio": ["son", "audio", "qualité", "musique", "basses", "aigu", "aigus", "médiums", "clarté", "sonorité"],
                "anc": ["réduction", "bruit", "anc", "isolation", "bruits", "ambiant", "extérieur", "transparence", "bloquer"],
                "batterie": ["batterie", "autonomie", "charge", "boîtier", "charger", "tient", "heures", "autonomie"]
            },
            "phone": {
                "ecran": ["écran", "ecran", "dalle", "luminosité", "lumineux", "affichage", "couleurs", "tactile", "reflets"],
                "batterie": ["batterie", "autonomie", "charge", "charger", "chargeur", "tient", "jours", "heures"],
                "photo": ["photo", "photos", "appareil photo", "caméra", "zoom", "optique", "capteur", "nuit", "vidéo", "pixels"],
                "performance": ["rapide", "rapidité", "fluide", "fluidité", "processeur", "jeux", "ram", "chauffe", "chaud", "lenteur"],
                "design": ["design", "poids", "léger", "taille", "couleur", "dos", "matériaux", "prise en main", "ergonomie"],
                "ia": ["ia", "galaxy ai", "samsung ai", "intelligence artificielle", "gemini", "circle to search", "entourer pour rechercher", "assistant notes", "photo assist", "interprète", "traduction en temps réel", "traduction en direct"]
            },
            "tablet": {
                "ecran": ["écran", "ecran", "dalle", "luminosité", "affichage", "couleurs", "taille", "grand"],
                "batterie": ["batterie", "autonomie", "charge", "charger", "tient", "heures", "jours"],
                "spen": ["stylet", "s pen", "spen", "écriture", "dessin", "crayon", "prise de note"],
                "performance": ["rapide", "rapidité", "fluide", "fluidité", "processeur", "productivité", "travail"],
                "ergonomie": ["poids", "léger", "finesse", "fin", "prise en main", "lourd", "transporter"]
            },
            "tv": {
                "image": ["image", "images", "couleurs", "contraste", "noir", "noirs", "oled", "qled", "luminosité", "dalle", "4k", "8k"],
                "audio": ["son", "audio", "qualité", "haut-parleurs", "basses", "barre de son", "puissance"],
                "smart": ["smart", "tizen", "applications", "appli", "applis", "netflix", "youtube", "interface", "menu", "télécommande", "connecté"],
                "design": ["finesse", "fin", "cadre", "design", "esthétique", "pied", "accroche"]
            },
            "home_appliance": {
                "efficacite": ["efficace", "efficacité", "puissance", "aspiration", "nettoyage", "lavage", "séchage", "propre", "performance", "rapide", "cuisson"],
                "bruit": ["bruit", "silencieux", "sonore", "silence", "vibrations", "vibre", "ronflement", "décibels", "db", "bruyant"],
                "capacite": ["capacité", "place", "grand", "volume", "litres", "kg", "espace", "tambour", "tiroirs", "taille", "intérieur"],
                "utilisation": ["facile", "simple", "programme", "programmation", "fonctions", "connecté", "application", "smartthings", "ergonomie"]
            },
            "default": {
                "qualite": ["qualité", "robuste", "solide", "matériaux", "finition", "plastique"],
                "prix": ["prix", "cher", "chère", "rapport", "qualité-prix", "promotion", "offre", "coût"],
                "utilisation": ["facile", "simple", "utilisation", "prise en main", "ergonomie", "compliqué"]
            }
        }

    def get_product_category(self, product_name):
        """
        Deduce product category from its name to customize analyzed aspects.
        """
        name_lower = product_name.lower()
        if any(x in name_lower for x in ["watch", "montre", "fit"]):
            return "watch"
        elif any(x in name_lower for x in ["buds", "écouteurs", "casque", "audio"]):
            return "buds"
        elif any(x in name_lower for x in ["tab", "tablette"]):
            return "tablet"
        elif any(x in name_lower for x in ["tv", "téléviseur", "ecran", "monitor", "projecteur"]):
            return "tv"
        elif any(x in name_lower for x in ["galaxy s", "galaxy z", "fold", "flip", "galaxy a", "smartphone", "téléphone"]):
            return "phone"
        elif any(x in name_lower for x in ["bespoke", "laundry", "combo", "washer", "dryer", "aspirateur", "cleaner", "four", "refrigerateur", "réfrigérateur", "lave-linge", "lave linge", "seche-linge", "sèche linge", "lave-vaisselle", "lave vaisselle", "micro-ondes"]):
            return "home_appliance"
        else:
            return "default"

    def analyze(self, text, rating):
        """
        Analyze global sentiment based on text lexicons combined with review rating as a prior.
        """
        if not text:
            if rating >= 4:
                return "positive"
            elif rating <= 2:
                return "negative"
            else:
                return "neutral"
                
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        pos_count = 0
        neg_count = 0
        
        for w in words:
            if w in self.french_positive:
                pos_count += 1.2
            elif w in self.french_negative:
                neg_count += 1.2
            elif w in self.english_positive:
                pos_count += 1.0
            elif w in self.english_negative:
                neg_count += 1.0
                
        negations = ["pas", "non", "aucun", "aucune", "jamais", "rien", "ne"]
        for neg in negations:
            if neg in words:
                pos_count *= 0.5
                neg_count += 0.5
                
        score = pos_count - neg_count
        
        if rating >= 4:
            if score < -1.5: 
                return "neutral"
            return "positive"
        elif rating <= 2:
            if score > 1.5:
                return "neutral"
            return "negative"
        else: # rating == 3
            if score > 1.0:
                return "positive"
            elif score < -1.0:
                return "negative"
            return "neutral"

    def analyze_sentence_sentiment(self, sentence_text, global_rating):
        """
        Helper to analyze sentiment of a single isolated sentence.
        """
        words = re.findall(r'\b\w+\b', sentence_text.lower())
        pos_count = sum(1 for w in words if w in self.french_positive or w in self.english_positive)
        neg_count = sum(1 for w in words if w in self.french_negative or w in self.english_negative)
        
        # Adjust with negation
        for neg in ["pas", "non", "ne", "aucun", "jamais"]:
            if neg in words:
                pos_count *= 0.4
                neg_count += 0.6
                
        score = pos_count - neg_count
        if score > 0.3:
            return "positive"
        elif score < -0.3:
            return "negative"
        else:
            # Fallback to rating prior if text is neutral/unclear
            if global_rating >= 4:
                return "positive"
            elif global_rating <= 2:
                return "negative"
            return "neutral"

    def calculate_sentence_score(self, sentence_text, global_rating):
        sentence_lower = sentence_text.lower()
        words = re.findall(r'\b\w+\b', sentence_lower)
        if not words:
            return float(global_rating)
            
        strong_positives = {
            "excellent", "parfait", "génial", "géniale", "magnifique", "superbe", 
            "incroyable", "recommande", "meilleur", "meilleure", "adore", "adoré", "top",
            "parfaite", "parfaits", "extraordinaire", "merveux", "réussi"
        }
        strong_negatives = {
            "mauvais", "nul", "nulle", "horrible", "pire", "déçu", "déçue", "décevant", 
            "décevante", "regrette", "panne", "casse", "inutile", "terrible", "catastrophe"
        }
        
        pos_words = self.french_positive.union(self.english_positive)
        neg_words = self.french_negative.union(self.english_negative)
        
        # Add some highly relevant aspect words to the lexicons if they are missing
        pos_words.update(["silencieux", "silencieuse", "silence", "grand", "grande", "propre", "propres", "intuitif", "interactive", "confortable", "confortables", "solide", "solides", "robuste", "robustes", "pratique", "pratiques", "esthétique", "beau", "belle", "rapide", "rapides"])
        neg_words.update(["bruyant", "bruyante", "bruyants", "bruyantes", "vibration", "vibrations", "petit", "petite", "petits", "petites", "lent", "lente", "lents", "lentes", "compliqué", "compliquée", "difficile", "difficiles", "cher", "chère", "chers", "chères", "fragile", "fragiles"])
        
        intensifiers = {
            "très", "tres", "extrêmement", "extremement", "vraiment", "super", 
            "hyper", "trop", "plus", "beaucoup", "particulièrement", "particulierement",
            "extrémement", "tellement", "fortement"
        }
        negations = {
            "pas", "non", "aucun", "aucune", "jamais", "rien", "ne", "ni", "sans", "guerre"
        }
        
        word_weights = []
        has_pos = False
        has_neg = False
        
        for idx, w in enumerate(words):
            is_pos = w in pos_words
            is_neg = w in neg_words
            
            if not is_pos and not is_neg:
                continue
                
            # Look at context (up to 2 words before)
            is_negated = False
            is_intensified = False
            
            for j in range(max(0, idx - 2), idx):
                prev_word = words[j]
                if prev_word in negations:
                    is_negated = True
                if prev_word in intensifiers:
                    is_intensified = True
                    
            # Base value
            val = 1.0
            if w in strong_positives or w in strong_negatives:
                val = 1.5
                
            if is_pos:
                if is_negated:
                    word_weights.append(-val * 1.2)
                    has_neg = True
                else:
                    word_weights.append(val * (1.5 if is_intensified else 1.0))
                    has_pos = True
            elif is_neg:
                if is_negated:
                    word_weights.append(val * 0.8) # e.g. "pas déçu" -> positive
                    has_pos = True
                else:
                    word_weights.append(-val * (1.5 if is_intensified else 1.0))
                    has_neg = True
                    
        if not word_weights:
            return float(global_rating)
            
        total_weight = sum(word_weights)
        
        # Convert weight to 1.0 - 5.0 score
        if total_weight > 0:
            # Positive sentiment
            if not has_neg and any(w in strong_positives for w in words):
                score = 5.0
            else:
                score = 3.0 + min(2.0, total_weight)
        elif total_weight < 0:
            # Negative sentiment
            if not has_pos and any(w in strong_negatives for w in words):
                score = 1.0
            else:
                score = 3.0 - min(2.0, abs(total_weight))
        else:
            score = 3.0
            
        # Ensure bounds
        score = max(1.0, min(5.0, score))
        return round(score, 1)

    def analyze_aspects(self, text, rating, category):
        """
        Aspect-Based Sentiment Analysis (ABSA).
        Splits review text into sentences, maps them to product aspects,
        and scores the aspect-specific sentiment and numerical rating.
        """
        if not text:
            return {}, {}

        aspects_config = self.ASPECTS_MAP.get(category, self.ASPECTS_MAP["default"])
        results = {}
        scores = {}

        # Split review into sentences/clauses
        sentences = re.split(r'[.,;!\n\r]+', text)
        
        for sentence in sentences:
            sentence_clean = sentence.strip()
            if len(sentence_clean) < 4:
                continue
                
            sentence_lower = sentence_clean.lower()
            
            # Check which aspects are mentioned in this specific sentence
            for aspect_name, keywords in aspects_config.items():
                # If any keyword matches
                if any(re.search(r'\b' + re.escape(kw) + r'\b', sentence_lower) for kw in keywords):
                    # Analyze the sentiment of this specific clause
                    sentiment = self.analyze_sentence_sentiment(sentence_clean, rating)
                    score = self.calculate_sentence_score(sentence_clean, rating)
                    # Store result (last mentioned takes precedence or positive/negative overwrite neutral)
                    if aspect_name not in results or results[aspect_name] == "neutral":
                        results[aspect_name] = sentiment
                        scores[aspect_name] = score
                        
        return results, scores
