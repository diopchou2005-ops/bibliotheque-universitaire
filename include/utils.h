#ifndef UTILS_H
#define UTILS_H

/*
 * DÃ©clarations des utilitaires de gÃ©nÃ©ration et d'affichage.
 * Elles servent aux programmes principaux et au benchmark.
 */

#include "structure.h"

Ouvrage ouvrage_aleatoire(int id);
void    ouvrage_afficher(const Ouvrage *ouvrage);

#endif