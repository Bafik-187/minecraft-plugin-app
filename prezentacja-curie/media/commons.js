/* Zweryfikowane pliki z Wikimedia Commons, ładowane online po nazwie pliku.
   f   – nazwy plików (sprawdzane po kolei), lic – licencja, by – autor/źródło.
   Pliki lokalne w media/ (np. media/<id>.jpg) mają pierwszeństwo. */
window.COMMONS = {
  /* --- portrety Marii --- */
  portret_1920:       {f:["Marie Curie c1920.jpg"], lic:"domena publiczna", by:"autor nieznany, ok. 1920"},
  portret_mlody:      {f:["Marie Curie 1903.jpg", "Mariecurie.jpg"], lic:"domena publiczna", by:"zdjęcie noblowskie, 1903"},
  portret_nobel:      {f:["Marie Curie (Nobel-Chem).jpg"], lic:"domena publiczna", by:"Fundacja Nobla, 1911"},
  student_1895:       {f:["Marie Sklodowska, étudiante, en 1895.jpg"], lic:"domena publiczna", by:"Maria jako studentka w Paryżu, 1895"},
  maria_uczennica:    {f:["Marie Sklodowska 16 years old.jpg"], lic:"domena publiczna", by:"z książki H. Skłodowskiej-Szalay, 1883"},
  siostry_1886:       {f:["Maria Sklodowska et sa sœur Bronislawa en 1886.jpg"], lic:"domena publiczna", by:"Maria i Bronisława, ok. 1886"},
  maria_1906:         {f:["Marie Curie in her laboratory.jpg"], lic:"domena publiczna", by:"autor nieznany, 1900s"},
  /* --- rodzina --- */
  rodzice:            {f:["Rodzice Marii Skłodowskiej (ok. 1870).jpg"], lic:"domena publiczna", by:"AGH, ok. 1870"},
  rodzina:            {f:["Sklodowski Family Wladyslaw and his daughters Maria Bronislawa Helena.jpg"], lic:"domena publiczna", by:"z książki H. Skłodowskiej-Szalay, 1890"},
  bronislawa:         {f:["Bronisława Dłuska (-1901).jpg"], lic:"domena publiczna", by:"Bronisława Dłuska, przed 1901"},
  piotr:              {f:["Pierre Curie by Dujardin c1906.jpg", "Pierrecurie.jpg"], lic:"domena publiczna", by:"Dujardin, ok. 1906"},
  slub_rowery:        {f:["Pierre et Marie Curie devant leur maison de Sceaux en 1895.jpg", "Pierre Curie et Marie Sklodowska Curie 1895.jpg"], lic:"zob. stronę pliku", by:"Boyer-Viollet, 1895 (archiwum ACJC)"},
  corki:              {f:["Eve, Marie, Irene Curie 1908.jpg"], lic:"CC BY 4.0", by:"Wellcome Collection, 1908"},
  irene:              {f:["Irène Joliot-Curie (1897-1956), c. 1935.jpg"], lic:"bez znanych ograniczeń", by:"Smithsonian Institution Archives"},
  eve:                {f:["Ève Curie.jpg"], lic:"domena publiczna (USA)", by:"1921"},
  /* --- nauka --- */
  laboratorium_curie: {f:["Pierre and Marie Curie.jpg"], lic:"domena publiczna", by:"przed 1906"},
  lab_wellcome:       {f:["Pierre and Marie Curie at work in laboratory Wellcome L0001761.jpg"], lic:"CC BY 4.0", by:"Wellcome Collection"},
  castaigne:          {f:["Curie and radium by Castaigne.jpg"], lic:"domena publiczna", by:"André Castaigne, 1904"},
  elektrometr:        {f:["Quadrant electrometer built by Pierre Curie, 1880-1890. (9660571325).jpg", "Electrometer (quadrant type) constructed by Pierre Curie. Wellcome M0011486.jpg"], lic:"zob. stronę pliku", by:"Science Museum London"},
  aparatura:          {f:["Original apparatus belonging to Marie Curie Wellcome M0011485.jpg"], lic:"CC BY 4.0", by:"Wellcome Collection"},
  rad_pomiary:        {f:["Measurement of Radium tubes at the Raduim Institute. Wellcome M0015305.jpg"], lic:"CC BY 4.0", by:"Wellcome Collection"},
  instytut_paryz:     {f:["MCP1642.jpg"], lic:"zob. stronę pliku", by:"Musée Curie, ok. 1920"},
  /* --- wojna, Ameryka, Warszawa, pamięć --- */
  rtg_ambulans:       {f:["Marie Curie - Mobile X-Ray-Unit.jpg"], lic:"domena publiczna", by:"z książki È. Curie „Madame Curie”, ok. 1915"},
  rtg_dawny:          {f:["Early x-ray procedure.jpg"], lic:"zob. stronę pliku", by:"Wikimedia Commons"},
  harding:            {f:["Pres. Warren G. Harding escorting Madame Curie down steps to south grounds of the White House LCCN93512088.jpg"], lic:"domena publiczna", by:"Library of Congress, 20 V 1921"},
  dluska_1932:        {f:["Bronisława Dłuska (Instytut Radowy 1932).jpg"], lic:"domena publiczna", by:"otwarcie Instytutu Radowego, 1932"},
  warszawa_kamienice: {f:["Warszawa-Rynek Starego Miasta-XIX.jpg"], lic:"domena publiczna", by:"autor nieznany, 1882–1888"},
  panteon:            {f:["Panthéon Pierre et Marie Curie.JPG"], lic:"zob. stronę pliku", by:"zdjęcie własne autora, 2011"}
};

/* Zweryfikowane filmy z Wikimedia Commons (ładowane online). */
window.COMMONS_VIDEO = {
  film_paryz_lumiere: {f:"A Trip Through Paris, France, Late 1890s.webm", lic:"domena publiczna", by:"firma Lumière, 1896–1900"},
  film_paryz_1900:    {f:"A Trip Through Paris, France, Late 1890s.webm", t:150, lic:"domena publiczna", by:"firma Lumière, 1896–1900"},
  film_rtg:           {f:"Dr. MacIntyre's X-Ray film.webm", lic:"domena publiczna", by:"dr John Macintyre, 1896–1909"}
};
