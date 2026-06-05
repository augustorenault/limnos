/** Horário de atendimento da matriz Limnos (Vespasiano/MG). */

export const openingHoursSpecification = [
  {
    '@type': 'OpeningHoursSpecification',
    dayOfWeek: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
    opens: '08:00',
    closes: '18:00',
  },
] as const;

/** Formato compacto aceito pelo Google (schema.org openingHours). */
export const openingHoursText = ['Mo-Fr 08:00-18:00'] as const;

export const hoursSummary = {
  weekdays: 'Segunda a sexta-feira: 08:00–18:00',
  weekend: 'Sábado e domingo: Fechado',
} as const;

export const hoursShort = 'Seg. a sex.: 08:00–18:00';
