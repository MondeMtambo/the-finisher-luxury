const skinTones = [
  { name: 'Porcelain', color: '#FCE2C4' },
  { name: 'Peach', color: '#E8B896' },
  { name: 'Olive', color: '#B98358' },
  { name: 'Mahogany', color: '#6B4226' },
  { name: 'Espresso', color: '#3A2318' }
];

const m1 = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <defs>
    <clipPath id="c_m1"><circle cx="50" cy="50" r="50"/></clipPath>
    <linearGradient id="bg_m1" x1="0" y1="0" x2="100" y2="100">
      <stop offset="0%" stop-color="#1A1D24"/>
      <stop offset="100%" stop-color="#000000"/>
    </linearGradient>
  </defs>
  <g clip-path="url(#c_m1)">
    <rect width="100" height="100" fill="url(#bg_m1)"/>
    <path d="M 10 100 Q 10 60 50 60 Q 90 60 90 100 Z" fill="#111418"/>
    <path d="M 35 100 L 50 75 L 65 100 Z" fill="#ffffff"/>
    <path d="M 47 75 L 53 75 L 55 100 L 45 100 Z" fill="#D4AF37"/>
    <rect x="42" y="45" width="16" height="20" fill="[SKIN_COLOR]"/>
    <circle cx="50" cy="38" r="18" fill="[SKIN_COLOR]"/>
    <path d="M 32 38 Q 32 15 50 15 Q 68 15 68 38 Q 68 25 50 20 Q 32 25 32 38 Z" fill="#111111"/>
  </g>
</svg>`;

const m2 = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <defs>
    <clipPath id="c_m2"><circle cx="50" cy="50" r="50"/></clipPath>
    <linearGradient id="bg_m2" x1="0" y1="0" x2="100" y2="100">
      <stop offset="0%" stop-color="#000000"/>
      <stop offset="100%" stop-color="#111418"/>
    </linearGradient>
  </defs>
  <g clip-path="url(#c_m2)">
    <rect width="100" height="100" fill="url(#bg_m2)"/>
    <path d="M 15 100 Q 15 65 50 65 Q 85 65 85 100 Z" fill="#D4AF37"/>
    <path d="M 35 100 L 35 60 Q 50 75 65 60 L 65 100 Z" fill="#111418"/>
    <rect x="42" y="40" width="16" height="20" fill="[SKIN_COLOR]"/>
    <circle cx="50" cy="35" r="18" fill="[SKIN_COLOR]"/>
    <rect x="34" y="32" width="12" height="8" rx="2" fill="none" stroke="#D4AF37" stroke-width="2"/>
    <rect x="54" y="32" width="12" height="8" rx="2" fill="none" stroke="#D4AF37" stroke-width="2"/>
    <line x1="46" y1="36" x2="54" y2="36" stroke="#D4AF37" stroke-width="2"/>
    <path d="M 32 35 C 32 10 68 10 68 35 C 68 20 32 20 32 35 Z" fill="#111111"/>
  </g>
</svg>`;

const f1 = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <defs>
    <clipPath id="c_f1"><circle cx="50" cy="50" r="50"/></clipPath>
    <linearGradient id="bg_f1" x1="0" y1="0" x2="100" y2="100">
      <stop offset="0%" stop-color="#111418"/>
      <stop offset="100%" stop-color="#000000"/>
    </linearGradient>
  </defs>
  <g clip-path="url(#c_f1)">
    <rect width="100" height="100" fill="url(#bg_f1)"/>
    <path d="M 15 100 Q 15 65 50 65 Q 85 65 85 100 Z" fill="#374151"/>
    <path d="M 35 100 L 50 75 L 65 100 Z" fill="#0B0C10"/>
    <path d="M 40 70 Q 50 85 60 70" fill="none" stroke="#D4AF37" stroke-width="2"/>
    <rect x="43" y="45" width="14" height="20" fill="[SKIN_COLOR]"/>
    <circle cx="50" cy="40" r="17" fill="[SKIN_COLOR]"/>
    <path d="M 30 50 Q 30 15 50 15 Q 70 15 70 50 Q 65 55 60 50 L 60 25 Q 50 20 40 25 L 40 50 Q 35 55 30 50 Z" fill="#111111"/>
  </g>
</svg>`;

const f2 = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <defs>
    <clipPath id="c_f2"><circle cx="50" cy="50" r="50"/></clipPath>
    <linearGradient id="bg_f2" x1="0" y1="0" x2="100" y2="100">
      <stop offset="0%" stop-color="#374151"/>
      <stop offset="100%" stop-color="#0B0C10"/>
    </linearGradient>
  </defs>
  <g clip-path="url(#c_f2)">
    <rect width="100" height="100" fill="url(#bg_f2)"/>
    <path d="M 20 100 Q 20 70 50 70 Q 80 70 80 100 Z" fill="#ffffff"/>
    <path d="M 40 100 Q 50 65 60 100 Z" fill="#D4AF37"/>
    <path d="M 35 75 Q 50 85 65 75 Z" fill="#B49015"/>
    <rect x="44" y="45" width="12" height="20" fill="[SKIN_COLOR]"/>
    <circle cx="50" cy="40" r="16" fill="[SKIN_COLOR]"/>
    <circle cx="50" cy="18" r="10" fill="#111111"/>
    <path d="M 33 40 Q 33 15 50 20 Q 67 15 67 40 Q 67 25 50 25 Q 33 25 33 40 Z" fill="#111111"/>
  </g>
</svg>`;

const templates = [
  { id: 'm1', gender: 'male', style: 'Executive Suit', svg: m1 },
  { id: 'm2', gender: 'male', style: 'Creative Director', svg: m2 },
  { id: 'f1', gender: 'female', style: 'Power Blazer', svg: f1 },
  { id: 'f2', gender: 'female', style: 'Elegant Blouse', svg: f2 }
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
