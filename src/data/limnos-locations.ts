/** Unidades físicas da Limnos (NAP + links de mapa). */

export const limnosFoundingYear = 1991;

export const limnosContacts = {
  telephone: '+553134271600',
  email: 'propostas@limnos.com.br',
  whatsapp: '+553185275215',
  whatsappDisplay: '(31) 8527-5215',
} as const;

/** Link wa.me — abre app no celular e WhatsApp Web no desktop */
export const limnosWhatsAppUrl =
  'https://wa.me/553185275215?text=' +
  encodeURIComponent('Olá! Gostaria de mais informações sobre as análises da Limnos');

export const limnosMatriz = {
  schemaId: 'localbusiness-matriz',
  schemaName: 'Limnos - Matriz (Vespasiano/MG)',
  heading: 'Matriz',
  streetAddress: 'Rua Paraíba, 1213 – Celvia',
  addressLocality: 'Vespasiano',
  addressRegion: 'MG',
  postalCode: '33200-640',
  mapsUrl: 'https://g.page/limnoslab',
  mapsTitle: 'Ver matriz Limnos no Google Maps',
  geo: {
    latitude: -19.69184148164372,
    longitude: -43.94154082477915,
  },
} as const;

export const limnosParauapebas = {
  schemaId: 'localbusiness-parauapebas',
  schemaName: 'Limnos - Unidade Parauapebas (PA)',
  heading: 'Unidade Parauapebas',
  streetAddress: 'Avenida I, Lote 43, Quadra 42',
  addressLocality: 'Cidade Jardim, Parauapebas',
  addressRegion: 'PA',
  postalCode: '68515-000',
  mapsUrl:
    'https://www.google.com/maps/search/?api=1&query=Avenida+I%2C+Lote+43%2C+Quadra+42+-+Cidade+Jardim%2C+Parauapebas+-+PA+68515-000',
  mapsTitle: 'Ver laboratório Parauapebas Limnos no Google Maps',
  note:
    'Unidade técnica de apoio às operações na região Norte. Visitas mediante agendamento.',
  schemaDescription:
    'Unidade técnica da Limnos em Parauapebas/PA, de apoio às operações na região Norte. Visitas mediante agendamento.',
} as const;
