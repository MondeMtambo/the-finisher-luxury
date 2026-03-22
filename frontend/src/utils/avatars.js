const skinTones = [
  { name: 'Porcelain', color: '#FCE2C4' },
  { name: 'Peach', color: '#E8B896' },
  { name: 'Olive', color: '#B98358' },
  { name: 'Mahogany', color: '#6B4226' },
  { name: 'Espresso', color: '#3A2318' }
];

const m1 = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <defs>
    <clipPath id="clip1"><circle cx="50" cy="50" r="50"/></clipPath>
    <linearGradient id="bg1" x1="0" y1="0" x2="100" y2="100">
      <stop offset="0%" stop-color="#1A1D24"/>
      <stop offset="100%" stop-color="#000000"/>
    </linearGradient>
  </defs>
  <g clip-path="url(#clip1)">
    <rect width="100" height="100" fill="url(#bg1)"/>
    <path d="M 10 110 C 25 70 75 70 90 110" fill="#0B0C10" stroke="#D4AF37" stroke-width="2"/>
    <path d="M 35 110 L 50 80 L 65 110" fill="#E5E7EB"/>
    <path d="M 46 80 L 54 80 L 56 110 L 44 110 Z" fill="#D4AF37"/>
    <rect x="42" y="60" width="16" height="25" fill="[SKIN_COLOR]"/>
    <path d="M 28 50 C 28 85 72 85 72 50 C 72 20 28 20 28 50 Z" fill="[SKIN_COLOR]"/>
    <path d="M 26 50 C 26 5 74 5 74 50 C 74 35 50 25 26 50 Z" fill="#111111"/>
  </g>
</svg>`;

const m2 = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <defs>
    <clipPath id="clip2"><circle cx="50" cy="50" r="50"/></clipPath>
    <linearGradient id="bg2" x1="0" y1="0" x2="100" y2="100">
      <stop offset="0%" stop-color="#2a2d34"/>
      <stop offset="100%" stop-color="#050505"/>
    </linearGradient>
  </defs>
  <g clip-path="url(#clip2)">
    <rect width="100" height="100" fill="url(#bg2)"/>
    <path d="M 15 110 C 20 65 80 65 85 110" fill="#111418"/>
    <path d="M 38 75 C 38 65 62 65 62 75 L 65 110 L 35 110 Z" fill="#0B0C10" stroke="#D4AF37" stroke-width="1"/>
    <rect x="42" y="55" width="16" height="20" fill="[SKIN_COLOR]"/>
    <path d="M 30 48 C 30 80 70 80 70 48 C 70 15 30 15 30 48 Z" fill="[SKIN_COLOR]"/>
    <rect x="30" y="42" width="16" height="12" rx="4" fill="none" stroke="#D4AF37" stroke-width="2.5"/>
    <rect x="54" y="42" width="16" height="12" rx="4" fill="none" stroke="#D4AF37" stroke-width="2.5"/>
    <line x1="46" y1="48" x2="54" y2="48" stroke="#D4AF37" stroke-width="2.5"/>
    <path d="M 28 48 C 28 10 72 10 72 48 C 72 35 28 35 28 48 Z" fill="#111111"/>
  </g>
</svg>`;

const f1 = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <defs>
    <clipPath id="clip3"><circle cx="50" cy="50" r="50"/></clipPath>
    <linearGradient id="bg3" x1="0" y1="0" x2="100" y2="100">
      <stop offset="0%" stop-color="#1A1D24"/>
      <stop offset="100%" stop-color="#000000"/>
    </linearGradient>
  </defs>
  <g clip-path="url(#clip3)">
    <rect width="100" height="100" fill="url(#bg3)"/>
    <path d="M 12 110 C 12 65 88 65 88 110" fill="#1F2937" stroke="#D4AF37" stroke-width="1.5"/>
    <path d="M 38 110 L 50 85 L 62 110" fill="#0B0C10"/>
    <rect x="43" y="60" width="14" height="30" fill="[SKIN_COLOR]"/>
    <path d="M 32 50 C 32 80 68 80 68 50 C 68 20 32 20 32 50 Z" fill="[SKIN_COLOR]"/>
    <path d="M 25 55 C 25 5 75 5 75 55 C 75 75 68 80 65 60 C 65 30 35 30 35 60 C 32 80 25 75 25 55 Z" fill="#0B0C10"/>
  </g>
</svg>`;

const f2 = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <defs>
    <clipPath id="clip4"><circle cx="50" cy="50" r="50"/></clipPath>
    <linearGradient id="bg4" x1="0" y1="0" x2="100" y2="100">
      <stop offset="0%" stop-color="#2a2d34"/>
      <stop offset="100%" stop-color="#050505"/>
    </linearGradient>
  </defs>
  <g clip-path="url(#clip4)">
    <rect width="100" height="100" fill="url(#bg4)"/>
    <path d="M 20 110 C 30 75 70 75 80 110" fill="#E5E7EB"/>
    <path d="M 40 85 Q 50 100 60 85" fill="none" stroke="#D4AF37" stroke-width="2.5"/>
    <rect x="44" y="60" width="12" height="30" fill="[SKIN_COLOR]"/>
    <path d="M 34 50 C 34 78 66 78 66 50 C 66 22 34 22 34 50 Z" fill="[SKIN_COLOR]"/>
    <circle cx="50" cy="20" r="16" fill="#0B0C10"/>
    <path d="M 30 48 C 30 15 70 15 70 48 C 70 30 30 30 30 48 Z" fill="#0B0C10"/>
  </g>
</svg>`;

const templates = [
  { id: 'm1', gender: 'male', style: 'Executive Fade', svg: m1 },
  { id: 'm2', gender: 'male', style: 'Modern Tech', svg: m2 },
  { id: 'f1', gender: 'female', style: 'Power Bob', svg: f1 },
  { id: 'f2', gender: 'female', style: 'Minimalist Updo', svg: f2 }
];

export const avatars = [];
templates.forEach(template => {
  skinTones.forEach((skin, index) => {
    avatars.push({
      id: `${template.id}-${index}`,
      gender: template.gender,
      style: template.style,
      skinTone: skin.name,
      svg: template.svg.replace(/\[SKIN_COLOR\]/g, skin.color)
    });
  });
});

export const getAvatarById = (id) => avatars.find(a => a.id === id) || avatars[0];
export const getRandomAvatar = () => avatars[Math.floor(Math.random() * avatars.length)];
