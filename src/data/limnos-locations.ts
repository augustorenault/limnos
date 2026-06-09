/** Unidades físicas da LIMNOS (NAP + links de mapa). */

export const LIMNOSFoundingYear = 1991;

export const LIMNOSContacts = {
  telephone: '+553134271600',
  email: 'propostas@LIMNOS.com.br',
  whatsapp: '+553185275215',
  whatsappDisplay: '(31) 8527-5215',
} as const;

/** Link wa.me — abre app no celular e WhatsApp Web no desktop */
export const LIMNOSWhatsAppUrl =
  'https://wa.me/553185275215?text=' +
  encodeURIComponent('Olá! Gostaria de mais informações sobre as análises da LIMNOS');

export const LIMNOSMatriz = {
  schemaId: 'localbusiness-matriz',
  schemaName: 'LIMNOS - Matriz (Vespasiano/MG)',
  heading: 'Matriz',
  streetAddress: 'Rua Paraíba, 1213 – Celvia',
  addressLocality: 'Vespasiano',
  addressRegion: 'MG',
  postalCode: '33200-640',
  mapsUrl: 'https://g.page/LIMNOSlab',
  mapsTitle: 'Ver matriz LIMNOS no Google Maps',
  geo: {
    latitude: -19.69184148164372,
    longitude: -43.94154082477915,
  },
} as const;

export const LIMNOSParauapebas = {
  schemaId: 'localbusiness-parauapebas',
  schemaName: 'LIMNOS - Unidade Parauapebas (PA)',
  heading: 'Unidade Parauapebas',
  streetAddress: 'Avenida I, Lote 43, Quadra 42',
  addressLocality: 'Cidade Jardim, Parauapebas',
  addressRegion: 'PA',
  postalCode: '68515-000',
  mapsUrl:
    'https://www.google.com/maps/search/?api=1&query=Avenida+I%2C+Lote+43%2C+Quadra+42+-+Cidade+Jardim%2C+Parauapebas+-+PA+68515-000',
  mapsTitle: 'Ver laboratório Parauapebas LIMNOS no Google Maps',
  note:
    'Unidade técnica de apoio às operações na região Norte. Visitas mediante agendamento.',
  schemaDescription:
    'Unidade técnica da LIMNOS em Parauapebas/PA, de apoio às operações na região Norte. Visitas mediante agendamento.',
} as const;
