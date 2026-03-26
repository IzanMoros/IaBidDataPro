# -*- coding: utf-8 -*-
"""
Dataset de Películas para Recomendación Semántica
==================================================

Este módulo contiene un dataset curado de películas con descripciones
ricas en emociones y temas para demostrar búsqueda semántica.

Las descripciones están diseñadas para capturar:
- Emociones que transmite la película
- Temas principales
- Ambientación
- Tono narrativo

Esto permite que el sistema entienda búsquedas como:
"algo triste en el espacio" → Interstellar
"""

import pandas as pd


def obtener_dataset_peliculas():
    """
    Retorna un DataFrame con películas y sus descripciones semánticas.
    
    Returns:
        pd.DataFrame: Dataset con columnas [titulo, año, genero, descripcion]
    
    Nota: Las descripciones están optimizadas para embeddings semánticos,
    no son sinopsis tradicionales.
    """
    
    # Dataset curado con descripciones emocionales y temáticas
    peliculas = [
        {
            "titulo": "Interstellar",
            "año": 2014,
            "genero": "Ciencia Ficción",
            "descripcion": "Una historia emocionalmente desgarradora sobre un padre separado de su hija mientras viaja por el espacio profundo. Explora temas de tiempo, amor, sacrificio y la soledad del cosmos. Mezcla ciencia dura con momentos profundamente emotivos y reflexivos sobre la humanidad."
        },
        {
            "titulo": "Deadpool",
            "año": 2016,
            "genero": "Acción/Comedia",
            "descripcion": "Comedia irreverente y extremadamente divertida sobre un antihéroe con superpoderes. Llena de humor negro, acción violenta pero cómica, y constantes bromas rompiendo la cuarta pared. Perfecta para reír sin parar con escenas de acción espectaculares."
        },
        {
            "titulo": "The Shining",
            "año": 1980,
            "genero": "Terror",
            "descripcion": "Terror psicológico intenso ambientado en un hotel aislado en la montaña durante el invierno. Atmósfera opresiva y claustrofóbica que juega con la mente. Locura, aislamiento, y horror sobrenatural que te deja sin dormir. Lenta pero perturbadora."
        },
        {
            "titulo": "Amélie",
            "año": 2001,
            "genero": "Romance/Comedia",
            "descripcion": "Película encantadora y visualmente hermosa ambientada en el París bohemio. Historia tierna y caprichosa sobre una joven tímida que ayuda a otros a encontrar la felicidad mientras busca el amor. Llena de color, fantasía, y momentos que calientan el corazón."
        },
        {
            "titulo": "Requiem for a Dream",
            "año": 2000,
            "genero": "Drama",
            "descripcion": "Una de las películas más devastadoras y angustiantes sobre adicción y sueños rotos. Intensamente triste, oscura y perturbadora. Muestra la espiral descendente de varias vidas destruidas. No es fácil de ver pero imposible de olvidar."
        },
        {
            "titulo": "Guardians of the Galaxy",
            "año": 2014,
            "genero": "Ciencia Ficción/Comedia",
            "descripcion": "Aventura espacial divertidísima con superhéroes inadaptados. Llena de humor, música retro increíble, y acción colorida en el espacio. Tone ligero y entretenido con personajes carismáticos. Perfecta para pasar un buen rato sin complicaciones."
        },
        {
            "titulo": "Grave of the Fireflies",
            "año": 1988,
            "genero": "Animación/Drama",
            "descripcion": "Película de animación japonesa devastadoramente triste sobre dos hermanos durante la Segunda Guerra Mundial. Una de las historias más conmovedoras y desgarradoras sobre la pérdida, la guerra y la inocencia. Prepara muchos pañuelos."
        },
        {
            "titulo": "Hot Fuzz",
            "año": 2007,
            "genero": "Acción/Comedia",
            "descripcion": "Comedia británica hilarante que parodia las películas de acción. Ambientada en un pueblo aparentemente tranquilo con secretos oscuros. Brillantemente cómica con diálogos ingeniosos y escenas de acción absurdas pero espectaculares."
        },
        {
            "titulo": "Hereditary",
            "año": 2018,
            "genero": "Terror",
            "descripcion": "Terror psicológico perturbador sobre una familia atormentada por secretos oscuros y fuerzas sobrenaturales. Atmósfera opresiva y aterradora con giros impactantes. Horror que se queda en tu mente durante días. No apto para sensibles."
        },
        {
            "titulo": "Moonlight",
            "año": 2016,
            "genero": "Drama",
            "descripcion": "Drama íntimo y poético sobre identidad, amor y crecimiento personal en comunidades marginadas. Bellamente filmada, emocionalmente profunda y contemplativa. Explora la vulnerabilidad masculina y el autodescubrimiento con sensibilidad."
        },
        {
            "titulo": "Gravity",
            "año": 2013,
            "genero": "Ciencia Ficción/Thriller",
            "descripcion": "Thriller de supervivencia tenso y claustrofóbico ambientado completamente en el espacio. Sensación abrumadora de soledad y vacío cósmico. Visualmente impresionante con secuencias que quitan el aliento. Terror silencioso del espacio profundo."
        },
        {
            "titulo": "The Grand Budapest Hotel",
            "año": 2014,
            "genero": "Comedia/Drama",
            "descripcion": "Comedia visualmente deslumbrante con estética de cuento de hadas. Historia caprichosa y elegante sobre amistad, nostalgia y aventura en un hotel europeo ficticio. Diálogos ingeniosos, colores vibrantes y humor peculiar."
        },
        {
            "titulo": "Se7en",
            "año": 1995,
            "genero": "Thriller",
            "descripcion": "Thriller oscuro y perturbador sobre detectives persiguiendo a un asesino serial metódico. Atmósfera sombría y opresiva en una ciudad lluviosa decadente. Intensamente inquietante con un final devastador que te dejará sin palabras."
        },
        {
            "titulo": "Up",
            "año": 2009,
            "genero": "Animación/Aventura",
            "descripcion": "Película de animación que te hace llorar en los primeros 10 minutos y luego te lleva en una aventura mágica. Temas profundos de pérdida, envejecimiento, y encontrar significado. Emotiva pero también llena de encanto y aventura."
        },
        {
            "titulo": "Mad Max: Fury Road",
            "año": 2015,
            "genero": "Acción",
            "descripcion": "Acción pura y frenética en un desierto post-apocalíptico. Persecuciones espectaculares sin descanso, visualmente alucinante. Adrenalina constante con poca trama pero coreografía de acción magistral. Experiencia cinematográfica salvaje."
        },
        {
            "titulo": "Her",
            "año": 2013,
            "genero": "Romance/Ciencia Ficción",
            "descripcion": "Romance inusual y melancólico entre un hombre solitario y una inteligencia artificial. Reflexiva y emotiva sobre amor, soledad y conexión en la era digital. Atmósfera contemplativa y hermosa cinematografía cálida."
        },
        {
            "titulo": "Parasite",
            "año": 2019,
            "genero": "Thriller/Drama",
            "descripcion": "Thriller social impredecible sobre desigualdad de clases. Empieza como comedia negra y evoluciona a drama tenso y perturbador. Giros inesperados, simbolismo rico y crítica social mordaz. Mantiene la tensión de principio a fin."
        },
        {
            "titulo": "The Truman Show",
            "año": 1998,
            "genero": "Drama/Ciencia Ficción",
            "descripcion": "Drama filosófico sobre un hombre que descubre que toda su vida es un reality show. Reflexivo sobre libre albedrío, realidad y control. Tiene momentos divertidos pero también profundamente inquietantes sobre la manipulación."
        },
        {
            "titulo": "Spirited Away",
            "año": 2001,
            "genero": "Animación/Fantasía",
            "descripcion": "Fantasía animada mágica y onírica sobre una niña en un mundo espiritual japonés. Visualmente asombrosa con criaturas fantásticas y momentos de asombro. Historia sobre crecimiento, valentía y magia con toques de melancolía."
        },
        {
            "titulo": "Blade Runner 2049",
            "año": 2017,
            "genero": "Ciencia Ficción",
            "descripcion": "Ciencia ficción contemplativa y visualmente hipnótica sobre existencia e identidad. Ritmo lento y atmosférico en una ciudad futurista distópica bajo lluvia constante. Belleza melancólica con reflexiones sobre qué significa ser humano."
        },
        {
            "titulo": "Midnight in Paris",
            "año": 2011,
            "genero": "Romance/Comedia",
            "descripcion": "Comedia romántica encantadora sobre un escritor que viaja al París de los años 20 cada medianoche. Ligera, caprichosa y llena de nostalgia. Celebra el arte, la literatura y el romance en la ciudad más hermosa del mundo."
        },
        {
            "titulo": "Get Out",
            "año": 2017,
            "genero": "Terror/Thriller",
            "descripcion": "Terror social incómodo y perturbador sobre racismo encubierto. Tensión creciente que te mantiene al borde del asiento. Inteligente, inquietante y con giros impactantes. Horror psicológico que hace pensar."
        },
        {
            "titulo": "Eternal Sunshine of the Spotless Mind",
            "año": 2004,
            "genero": "Romance/Ciencia Ficción",
            "descripcion": "Romance no convencional y profundamente emotivo sobre borrar recuerdos de un amor perdido. Narrativa fragmentada y onírica. Reflexivo sobre memoria, amor y dolor. Triste pero hermoso al mismo tiempo."
        },
        {
            "titulo": "Shaun of the Dead",
            "año": 2004,
            "genero": "Comedia/Terror",
            "descripcion": "Comedia de zombies británica hilarante que mezcla humor absurdo con gore. Divertida y entrañable con personajes torpes enfrentando el apocalipsis zombie. Perfecta combinación de risas y momentos de acción sangrienta."
        },
        {
            "titulo": "Arrival",
            "año": 2016,
            "genero": "Ciencia Ficción",
            "descripcion": "Ciencia ficción cerebral y emotiva sobre comunicación con alienígenas. Ritmo contemplativo con reflexiones sobre lenguaje, tiempo y pérdida. Intelectualmente estimulante pero también profundamente conmovedora. Requiere atención pero recompensa."
        },
        {
            "titulo": "The Lighthouse",
            "año": 2019,
            "genero": "Terror/Drama",
            "descripcion": "Drama psicológico claustrofóbico sobre dos fareros aislados en una isla remota. Atmósfera opresiva y descenso a la locura. Filmado en blanco y negro con diálogos arcaicos. Perturbador, extraño y hipnótico."
        },
        {
            "titulo": "CODA",
            "año": 2021,
            "genero": "Drama/Música",
            "descripcion": "Drama musical conmovedor sobre una adolescente oyente en una familia sorda. Historia tierna sobre identidad, familia y seguir tus sueños. Emotiva sin ser manipuladora, con actuaciones hermosas y momentos que te hacen llorar de alegría."
        },
        {
            "titulo": "Everything Everywhere All at Once",
            "año": 2022,
            "genero": "Ciencia Ficción/Comedia",
            "descripcion": "Caos multiversal absolutamente demente que mezcla comedia absurda, acción creativa y emoción genuina. Frenética, colorida y sorprendentemente emotiva sobre familia e identidad. Experiencia cinematográfica única y abrumadoramente imaginativa."
        },
        {
            "titulo": "The Witch",
            "año": 2015,
            "genero": "Terror",
            "descripcion": "Terror de época lento y atmosférico sobre una familia puritana en el bosque. Tensión creciente y terror psicológico con ambiente ominoso constante. Auténtico sabor histórico con horror sobrenatural inquietante."
        },
        {
            "titulo": "La La Land",
            "año": 2016,
            "genero": "Musical/Romance",
            "descripcion": "Musical romántico vibrante sobre soñadores en Los Ángeles. Visualmente deslumbrante con números musicales encantadores. Celebra el arte y la ambición pero también explora el sacrificio y el agridulce del amor y los sueños."
        },
        # NUEVAS PELÍCULAS - Ampliación del dataset
        {
            "titulo": "Whiplash",
            "año": 2014,
            "genero": "Drama/Música",
            "descripcion": "Drama intenso y estresante sobre un baterista ambicioso y su instructor abusivo. Tensión brutal y persecución obsesiva de la perfección. Secuencias musicales electrizantes con emociones al límite. Inquietante pero imposible de apartar la mirada."
        },
        {
            "titulo": "The Matrix",
            "año": 1999,
            "genero": "Ciencia Ficción/Acción",
            "descripcion": "Revolucionaria película de acción filosófica sobre realidad simulada y despertar de la conciencia. Coreografía de pelea innovadora y efectos visuales alucinantes. Exploración de libre albedrío y existencia con acción espectacular."
        },
        {
            "titulo": "A Quiet Place",
            "año": 2018,
            "genero": "Terror/Thriller",
            "descripcion": "Terror silencioso y tenso sobre una familia sobreviviendo en un mundo donde el sonido atrae monstruos letales. Atmósfera opresiva con silencios que te mantienen en vilo. Emotivo con lazos familiares fuertes bajo amenaza terrorífica constante."
        },
        {
            "titulo": "The Farewell",
            "año": 2019,
            "genero": "Drama/Comedia",
            "descripcion": "Drama agridulce sobre familia, cultura y mentiras piadosas en torno a una abuela enferma. Emotiva exploración de diferencias culturales entre Oriente y Occidente. Tierna, divertida y conmovedora sobre el amor familiar."
        },
        {
            "titulo": "Dune",
            "año": 2021,
            "genero": "Ciencia Ficción/Aventura",
            "descripcion": "Épica espacial visualmente espectacular en planetas desérticos con política compleja y profecías místicas. Cinematografía abrumadora con paisajes alienígenas monumentales. Atmósfera contemplativa mezclada con acción en gran escala."
        },
        {
            "titulo": "Joker",
            "año": 2019,
            "genero": "Drama/Thriller",
            "descripcion": "Descenso perturbador a la locura de un hombre marginado en una ciudad decadente. Oscuro, deprimente y profundamente incómodo. Actuación inquietante en un retrato brutal de enfermedad mental y fracaso social."
        },
        {
            "titulo": "The Secret Life of Walter Mitty",
            "año": 2013,
            "genero": "Aventura/Comedia",
            "descripcion": "Aventura inspiradora sobre un hombre tímido que embarca en un viaje épico alrededor del mundo. Visualmente hermosa con momentos de asombro y autodescubrimiento. Optimista y motivadora sobre atreverse a vivir plenamente."
        },
        {
            "titulo": "Midsommar",
            "año": 2019,
            "genero": "Terror",
            "descripcion": "Terror diurno perturbador en un festival pagano sueco. Brillantemente iluminado pero profundamente inquietante. Horror folklórico extraño y desconcertante que te deja incómodo. No usa oscuridad sino luz solar para crear terror."
        },
        {
            "titulo": "The Lion King",
            "año": 1994,
            "genero": "Animación/Musical",
            "descripcion": "Musical animado épico sobre un león joven que debe reclamar su lugar como rey. Emotivo con música icónica y momentos que te hacen llorar. Temas de pérdida, responsabilidad y círculo de la vida. Aventura mágica para todas las edades."
        },
        {
            "titulo": "Knives Out",
            "año": 2019,
            "genero": "Misterio/Comedia",
            "descripcion": "Misterio de asesinato ingenioso y divertido con giros constantes. Inteligente, entretenido y lleno de humor mordaz. Elenco carismático en una trama intrincada que mantiene adivinando. Moderna versión de Agatha Christie."
        },
        {
            "titulo": "Call Me By Your Name",
            "año": 2017,
            "genero": "Romance/Drama",
            "descripcion": "Romance veraniego languido y hermoso ambientado en la Italia rural. Cinematografía cálida, sensual y melancólica. Historia de amor tierna sobre descubrimiento y deseo con final agridulce. Emocionalmente devastador pero hermoso."
        },
        {
            "titulo": "The Social Network",
            "año": 2010,
            "genero": "Drama/Biográfico",
            "descripcion": "Drama rápido y ágil sobre la creación de Facebook y la traición entre amigos. Diálogos brillantes con ritmo frenético. Exploración de ambición, amistad y el precio del éxito en la era digital."
        },
        {
            "titulo": "Inception",
            "año": 2010,
            "genero": "Ciencia Ficción/Thriller",
            "descripcion": "Thriller de ciencia ficción cerebral sobre entrar en sueños dentro de sueños. Conceptualmente complejo con acción espectacular. Visualmente impresionante con secuencias que desafían la gravedad. Requiere atención total pero altamente gratificante."
        },
        {
            "titulo": "Room",
            "año": 2015,
            "genero": "Drama",
            "descripcion": "Drama devastador sobre una madre y su hijo cautivos en una habitación. Primera mitad claustrofóbica y opresiva, segunda mitad sobre redescubrimiento del mundo. Profundamente emotivo y desgarrador sobre amor maternal y trauma."
        },
        {
            "titulo": "Shutter Island",
            "año": 2010,
            "genero": "Thriller/Misterio",
            "descripcion": "Thriller psicológico oscuro y atmosférico en un asilo para criminales dementes en una isla remota. Tensión constante con giros que cuestionan la realidad. Perturbador y misterioso con revelaciones impactantes."
        },
        {
            "titulo": "Django Unchained",
            "año": 2012,
            "genero": "Western/Acción",
            "descripcion": "Western violento y estilizado sobre venganza y justicia en el sur esclavista. Mezcla humor negro con violencia gráfica. Diálogos ingeniosos en una historia brutal sobre esclavitud y redención violenta."
        },
        {
            "titulo": "The Handmaiden",
            "año": 2016,
            "genero": "Thriller/Romance",
            "descripcion": "Thriller erótico coreano con giros elaborados y seducción compleja. Visualmente suntuoso y sensual con narrativa laberíntica. Inteligente, provocativo y lleno de sorpresas sobre engaño, deseo y liberación."
        },
        {
            "titulo": "Hunt for the Wilderpeople",
            "año": 2016,
            "genero": "Comedia/Aventura",
            "descripcion": "Comedia neozelandesa encantadora sobre un niño rebelde y su tío huyendo al monte. Divertida y entrañable con humor peculiar. Historia de amistad poco probable con corazón genuino y momentos hilarantes."
        },
        {
            "titulo": "The Pianist",
            "año": 2002,
            "genero": "Drama/Bélico",
            "descripcion": "Drama devastador sobre un pianista judío sobreviviendo el Holocausto en la Varsovia ocupada. Brutalmente realista y desgarrador. Silencioso y contemplativo sobre supervivencia, pérdida y la música como refugio del horror."
        },
        {
            "titulo": "Baby Driver",
            "año": 2017,
            "genero": "Acción/Thriller",
            "descripcion": "Thriller de acción estilizado con persecuciones de autos sincronizadas perfectamente con música. Frenético, colorido y pulsante con edición impecable. Adrenalina pura con ritmo musical y romance juvenil."
        },
        {
            "titulo": "Schindler's List",
            "año": 1993,
            "genero": "Drama/Bélico",
            "descripcion": "Drama monumental y devastador sobre el Holocausto filmado en blanco y negro. Una de las películas más importantes y desgarradoras sobre humanidad en la oscuridad. Brutal, necesaria e inolvidable."
        },
        {
            "titulo": "The Sixth Sense",
            "año": 1999,
            "genero": "Thriller/Drama",
            "descripcion": "Thriller sobrenatural con uno de los giros más famosos del cine. Atmósfera inquietante y melancólica sobre un niño que ve muertos. Emotivo y escalofriante con final que recontextualiza todo."
        },
        {
            "titulo": "Black Swan",
            "año": 2010,
            "genero": "Thriller/Drama",
            "descripcion": "Thriller psicológico intenso sobre una bailarina obsesionada con la perfección que desciende a la locura. Perturbador y visceral con imágenes de terror psicológico. Actuación inquietante en descenso a la paranoia."
        },
        {
            "titulo": "Spider-Man: Into the Spider-Verse",
            "año": 2018,
            "genero": "Animación/Acción",
            "descripcion": "Animación revolucionaria visualmente alucinante con estilo de cómic en movimiento. Divertida, emotiva y espectacularmente creativa. Historia sobre identidad y potencial con acción frenética y corazón genuino."
        },
        {
            "titulo": "Prisoners",
            "año": 2013,
            "genero": "Thriller/Drama",
            "descripcion": "Thriller oscuro y brutal sobre un padre desesperado buscando a su hija secuestrada. Moralmente complejo y perturbador sobre hasta dónde llegarías por tu familia. Tenso, sombrío y emocionalmente agotador."
        },
        {
            "titulo": "Little Miss Sunshine",
            "año": 2006,
            "genero": "Comedia/Drama",
            "descripcion": "Comedia indie agridulce sobre una familia disfuncional en un viaje por carretera. Divertida y conmovedora con personajes excéntricos pero entrañables. Humor peculiar mezclado con momentos genuinamente emotivos sobre aceptación."
        },
        {
            "titulo": "The Prestige",
            "año": 2006,
            "genero": "Thriller/Misterio",
            "descripcion": "Thriller intrincado sobre rivalidad obsesiva entre magos victorianos. Narrativa compleja con capas sobre sacrificio y obsesión. Giros elaborados que requieren atención, atmósfera oscura del Londres victoriano."
        },
        {
            "titulo": "Pan's Labyrinth",
            "año": 2006,
            "genero": "Fantasía/Drama",
            "descripcion": "Cuento de hadas oscuro y violento ambientado en la España de la posguerra. Belleza visual onírica mezclada con brutalidad realista de guerra. Mágico pero devastador, inocencia en contraste con horror histórico."
        },
        {
            "titulo": "No Country for Old Men",
            "año": 2007,
            "genero": "Thriller/Western",
            "descripcion": "Thriller brutal y nihilista sobre un encuentro con un asesino implacable en el oeste de Texas. Tensión implacable con violencia súbita y atmosfera desolada. Reflexión oscura sobre el mal y el destino inevitable."
        },
        {
            "titulo": "The Shawshank Redemption",
            "año": 1994,
            "genero": "Drama",
            "descripcion": "Drama carcelario emotivo sobre esperanza, amistad y redención durante décadas de injusticia. Inspirador pero también brutal sobre la pérdida de libertad. Final que te hace llorar de alegría después de tanto sufrimiento."
        },
        # NUEVAS PELÍCULAS AÑADIDAS (ESPACIO, CIENCIA FICCIÓN, Y CLÁSICOS)
        {
            "titulo": "Star Wars: Una Nueva Esperanza",
            "año": 1977,
            "genero": "Ciencia Ficción/Aventura",
            "descripcion": "Aventura épica en una galaxia muy, muy lejana. Un joven descubre su destino en una rebelión espacial contra un imperio malvado. Acción clásica, espadas láser, naves espaciales, extraterrestres y la Fuerza misteriosa."
        },
        {
            "titulo": "Star Wars: El Imperio Contraataca",
            "año": 1980,
            "genero": "Ciencia Ficción/Aventura",
            "descripcion": "Secuela oscura y emocionante en la galaxia. Persecuciones en el espacio profundo, entrenamiento místico y una revelación familiar impactante. Combate espacial, planetas helados y una gran aventura de ciencia ficción."
        },
        {
            "titulo": "Avengers: Infinity War",
            "año": 2018,
            "genero": "Acción/Ciencia Ficción",
            "descripcion": "Superhéroes de toda la galaxia se unen para detener a un titán que amenaza con eliminar la mitad del universo. Acción deslumbrante, sacrificios trágicos y batallas épicas en diferentes planetas y la Tierra."
        },
        {
            "titulo": "The Martian (Marte)",
            "año": 2015,
            "genero": "Ciencia Ficción/Aventura",
            "descripcion": "Supervivencia realista e ingeniosa de un astronauta abandonado en Marte. Aventura de ciencia dura, optimismo, humor en situaciones límite y cooperación global para un rescate espacial interplanetario."
        },
        {
            "titulo": "Avatar",
            "año": 2009,
            "genero": "Ciencia Ficción/Aventura",
            "descripcion": "Espectáculo visual asombroso ambientado en el planeta alienígena Pandora. Un humano se infiltra en una tribu extraterrestre y cuestiona su lealtad ante la codicia militar. Conexión con la naturaleza y épicas batallas de ciencia ficción."
        },
        {
            "titulo": "WALL-E",
            "año": 2008,
            "genero": "Animación/Ciencia Ficción",
            "descripcion": "Animación conmovedora y casi sin diálogos sobre un pequeño robot solitario que limpia una Tierra post-apocalíptica y viaja al espacio. Romance tierno, sátira ecológica y aventura galáctica para toda la familia."
        },
        {
            "titulo": "Alien: El Octavo Pasajero",
            "año": 1979,
            "genero": "Terror/Ciencia Ficción",
            "descripcion": "Terror espacial claustrofóbico y magistral. La tripulación de una nave comercial es cazada por un aterrador organismo extraterrestre alienígena letal. Tensión pura en la oscuridad del espacio profundo."
        },
        {
            "titulo": "El Padrino",
            "año": 1972,
            "genero": "Crimen/Drama",
            "descripcion": "Drama épico sobre la familia mafiosa Corleone. Exploración de poder, la lealtad, la traición y el precio de proteger el legado familiar. Diálogos memorables e icónicos en una historia criminal oscura y compleja."
        },
        {
            "titulo": "Regreso al Futuro",
            "año": 1985,
            "genero": "Comedia/Ciencia Ficción",
            "descripcion": "Comedia de viajes en el tiempo muy divertida y entrañable. Un adolescente viaja accidentalmente a los años 50 en un DeLorean modificado. Aventura emocionante llena de ingenio y encanto nostálgico."
        },
        {
            "titulo": "Jurassic Park",
            "año": 1993,
            "genero": "Aventura/Ciencia Ficción",
            "descripcion": "Aventura de ciencia ficción y suspense donde los dinosaurios vuelven a la vida en un parque temático. Sentido de la maravilla seguido de terror aterrador e intenso cuando la naturaleza escapa del control humano."
        },
        {
            "titulo": "Terminator 2: El Juicio Final",
            "año": 1991,
            "genero": "Acción/Ciencia Ficción",
            "descripcion": "Película revolucionaria sobre cyborgs asesinos y un futuro apocalíptico controlado por inteligencia artificial. Secuencias de acción espectaculares, explosiones increíbles y una inesperada historia de figura paterna protectora."
        },
        {
            "titulo": "The Dark Knight",
            "año": 2008,
            "genero": "Acción/Thriller",
            "descripcion": "Thriller de superhéroes intenso y oscuro sobre la corrupción, el caos y la moralidad. Batman se enfrenta al perturbador y anárquico Joker. Dramática y criminal, mucho más que una película de cómics tradicional."
        },
        {
            "titulo": "Gladiator",
            "año": 2000,
            "genero": "Acción/Drama",
            "descripcion": "Épica histórica en la Antigua Roma de venganza y honor. Un general caído lucha en el coliseo para vengar a su familia. Batallas brutales y emotivas con un heroísmo inquebrantable y espectacular."
        },
        {
            "titulo": "Titanic",
            "año": 1997,
            "genero": "Romance/Drama",
            "descripcion": "Romance trágico y majestuoso superproducción a bordo del desafortunado transatlántico. Historia de amor clásico entre diferentes clases sociales seguido de un intenso drama de supervivencia durante el hundimiento."
        },
        {
            "titulo": "Toy Story",
            "año": 1995,
            "genero": "Animación/Aventura",
            "descripcion": "Animación pionera sobre la vida secreta de los juguetes. Una historia entrañable sobre celos, amistad y aceptación. Divertida, colorida y nostálgica experiencia infantil adorada por toda la familia."
        },
        {
            "titulo": "Forrest Gump",
            "año": 1994,
            "genero": "Drama/Comedia",
            "descripcion": "Comedia dramática emocional que sigue a un hombre de buen corazón a lo largo de décadas de historia estadounidense. Cuentos inspiradores sobre el destino, el amor incondicional y lograr lo extraordinario siendo uno mismo."
        },
        {
            "titulo": "E.T., el Extra-Terrestre",
            "año": 1982,
            "genero": "Ciencia Ficción/Familiar",
            "descripcion": "Película infantil mágica y profundamente emotiva sobre la amistad entre un niño solitario y un alienígena perdido de otra galaxia. Tierna, llena de maravilla y con un final desgarrador e inspirador."
        },
        {
            "titulo": "2001: Una Odisea del Espacio",
            "año": 1968,
            "genero": "Ciencia Ficción",
            "descripcion": "Obra maestra visual y filosófica de ritmo lento y contemplativo sobre la evolución y el cosmos. Una expedición espacial se enfrenta a una inteligencia artificial rebelde, HAL. Abstracta, espacial y misteriosa."
        },
        {
            "titulo": "Coco",
            "año": 2017,
            "genero": "Animación/Familiar",
            "descripcion": "Aventura animada visualmente deslumbrante sobre el Día de Muertos. Historia profundamente conmovedora sobre la memoria, la familia, y el amor a la música. Alegría vibrante que termina en lágrimas emocionales de felicidad."
        },
    ]
    
    return pd.DataFrame(peliculas)


def estadisticas_dataset():
    """
    Muestra estadísticas básicas del dataset.
    Útil para entender la composición de los datos.
    """
    df = obtener_dataset_peliculas()
    
    print("=" * 60)
    print("ESTADISTICAS DEL DATASET DE PELICULAS")
    print("=" * 60)
    print(f"\nTotal de peliculas: {len(df)}")
    print(f"Rango de años: {df['año'].min()} - {df['año'].max()}")
    print(f"\nDistribucion por genero:")
    print(df['genero'].value_counts().to_string())
    print(f"\nLongitud promedio de descripcion: {df['descripcion'].str.len().mean():.0f} caracteres")
    print("=" * 60)


# Ejecutar estadísticas si se ejecuta directamente
if __name__ == "__main__":
    estadisticas_dataset()
    
    # Mostrar algunas películas de ejemplo
    df = obtener_dataset_peliculas()
    print("\nEjemplos de peliculas:\n")
    print(df[['titulo', 'año', 'genero']].head(5).to_string(index=False))
