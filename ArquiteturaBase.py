from abc import ABC, abstractmethod
from typing import List, Tuple
import time

class SearchStrategy(ABC):
    """Interface para estratégias de busca"""

    @abstractmethod
    def search(self, text: str, pattern: str, step_by_step: bool = False) -> dict:
        """
        Executa a busca
        Retorna: {
            'matches': lista de índices,
            'comparisons': número de comparações,
            'time_ms': tempo em milissegundos,
            'steps': lista de passos (se step_by_step=True)
        }
        """
        pass


class NaiveSearch(SearchStrategy):
    """Busca Naive - Força Bruta O(n*m)"""

    def search(self, text: str, pattern: str, step_by_step: bool = False) -> dict:
        matches = []
        comparisons = 0
        steps = []

        start_time = time.perf_counter()

        for i in range(len(text) - len(pattern) + 1):
            if step_by_step:
                steps.append({
                    'position': i,
                    'action': f'Comparando posição {i}',
                    'text_window': text[i:i+len(pattern)],
                    'pattern': pattern
                })

            match = True
            for j in range(len(pattern)):
                comparisons += 1
                if text[i + j] != pattern[j]:
                    match = False
                    break

            if match:
                matches.append(i)
                if step_by_step:
                    steps.append({
                        'position': i,
                        'action': 'PADRÃO ENCONTRADO',
                        'match_index': i
                    })

        end_time = time.perf_counter()
        time_ms = (end_time - start_time) * 1000

        return {
            'algorithm': 'Naive Search',
            'matches': matches,
            'comparisons': comparisons,
            'time_ms': time_ms,
            'complexity': 'O(n * m)',
            'steps': steps if step_by_step else []
        }


class RabinKarpSearch(SearchStrategy):
    """Rabin-Karp - Hash O(n+m) médio"""

    def search(self, text: str, pattern: str, step_by_step: bool = False) -> dict:
        matches = []
        comparisons = 0
        steps = []

        # Parâmetros para hash
        prime = 101
        base = 256

        start_time = time.perf_counter()

        pattern_hash = 0
        text_hash = 0
        h = 1

        # Calcular h = base^(m-1) % prime
        for i in range(len(pattern) - 1):
            h = (h * base) % prime

        # Calcular hash do padrão e primeira janela
        for i in range(len(pattern)):
            pattern_hash = (base * pattern_hash + ord(pattern[i])) % prime
            text_hash = (base * text_hash + ord(text[i])) % prime

        if step_by_step:
            steps.append({
                'action': 'Inicialização',
                'pattern_hash': pattern_hash,
                'message': f'Hash do padrão: {pattern_hash}'
            })

        # Deslizar a janela
        for i in range(len(text) - len(pattern) + 1):
            comparisons += 1

            if step_by_step:
                steps.append({
                    'position': i,
                    'action': f'Comparando hash na posição {i}',
                    'text_window': text[i:i+len(pattern)],
                    'text_hash': text_hash,
                    'pattern_hash': pattern_hash
                })

            # Se hashes coincidem, verificar caractere por caractere
            if pattern_hash == text_hash:
                match = True
                for j in range(len(pattern)):
                    if text[i + j] != pattern[j]:
                        match = False
                        break

                if match:
                    matches.append(i)
                    if step_by_step:
                        steps.append({
                            'position': i,
                            'action': 'PADRÃO ENCONTRADO',
                            'match_index': i
                        })

            # Calcular hash da próxima janela
            if i < len(text) - len(pattern):
                text_hash = (base * (text_hash - ord(text[i]) * h) + ord(text[i + len(pattern)])) % prime
                if text_hash < 0:
                    text_hash += prime

        end_time = time.perf_counter()
        time_ms = (end_time - start_time) * 1000

        return {
            'algorithm': 'Rabin-Karp',
            'matches': matches,
            'comparisons': comparisons,
            'time_ms': time_ms,
            'complexity': 'O(n + m) médio',
            'steps': steps if step_by_step else []
        }


class KMPSearch(SearchStrategy):
    """Knuth-Morris-Pratt - O(n+m)"""

    def _build_lps(self, pattern: str) -> List[int]:
        """Constrói a tabela LPS (Longest Proper Prefix which is also Suffix)"""
        m = len(pattern)
        lps = [0] * m
        length = 0
        i = 1

        while i < m:
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1

        return lps

    def search(self, text: str, pattern: str, step_by_step: bool = False) -> dict:
        matches = []
        comparisons = 0
        steps = []

        start_time = time.perf_counter()

        lps = self._build_lps(pattern)

        if step_by_step:
            steps.append({
                'action': 'Tabela LPS construída',
                'lps_table': lps,
                'pattern': pattern
            })

        i = 0  # índice do texto
        j = 0  # índice do padrão

        while i < len(text):
            comparisons += 1

            if step_by_step:
                steps.append({
                    'text_index': i,
                    'pattern_index': j,
                    'action': f'Comparando text[{i}] com pattern[{j}]',
                    'text_char': text[i],
                    'pattern_char': pattern[j]
                })

            if pattern[j] == text[i]:
                i += 1
                j += 1

            if j == len(pattern):
                matches.append(i - j)
                if step_by_step:
                    steps.append({
                        'action': 'PADRÃO ENCONTRADO',
                        'match_index': i - j
                    })
                j = lps[j - 1]
            elif i < len(text) and pattern[j] != text[i]:
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1

        end_time = time.perf_counter()
        time_ms = (end_time - start_time) * 1000

        return {
            'algorithm': 'KMP (Knuth-Morris-Pratt)',
            'matches': matches,
            'comparisons': comparisons,
            'time_ms': time_ms,
            'complexity': 'O(n + m)',
            'lps_table': lps,
            'steps': steps if step_by_step else []
        }


class BoyerMooreSearch(SearchStrategy):
    """Boyer-Moore - O(n/m) melhor caso"""

    def _build_bad_char_table(self, pattern: str) -> dict:
        """Constrói tabela de saltos para caracteres ruins"""
        bad_char = {}
        for i in range(len(pattern)):
            bad_char[pattern[i]] = len(pattern) - i - 1
        return bad_char

    def search(self, text: str, pattern: str, step_by_step: bool = False) -> dict:
        matches = []
        comparisons = 0
        steps = []

        start_time = time.perf_counter()

        bad_char = self._build_bad_char_table(pattern)

        if step_by_step:
            steps.append({
                'action': 'Tabela de caracteres ruins construída',
                'bad_char_table': bad_char,
                'pattern': pattern
            })

        i = len(pattern) - 1  # índice no texto
        j = len(pattern) - 1  # índice no padrão

        while i < len(text):
            comparisons += 1

            if step_by_step:
                steps.append({
                    'text_index': i,
                    'pattern_index': j,
                    'action': f'Comparando text[{i}] com pattern[{j}]',
                    'text_char': text[i],
                    'pattern_char': pattern[j]
                })

            if text[i] == pattern[j]:
                if j == 0:
                    matches.append(i)
                    if step_by_step:
                        steps.append({
                            'action': 'PADRÃO ENCONTRADO',
                            'match_index': i
                        })
                    i += len(pattern)
                    j = len(pattern) - 1
                else:
                    i -= 1
                    j -= 1
            else:
                # Saltar usando tabela bad_char
                shift = bad_char.get(text[i], len(pattern))
                i += shift
                j = len(pattern) - 1

                if step_by_step:
                    steps.append({
                        'action': f'Caractere não encontrado, saltando {shift} posições',
                        'next_position': i
                    })

        end_time = time.perf_counter()
        time_ms = (end_time - start_time) * 1000

        return {
            'algorithm': 'Boyer-Moore',
            'matches': matches,
            'comparisons': comparisons,
            'time_ms': time_ms,
            'complexity': 'O(n / m) melhor caso',
            'bad_char_table': bad_char,
            'steps': steps if step_by_step else []
        }


class SearchComparator:
    """Comparador/unificador de estratégias de busca"""

    def __init__(self):
        self.algorithms = [
            NaiveSearch(),
            RabinKarpSearch(),
            KMPSearch(),
            BoyerMooreSearch()
        ]

    def search_all(self, text: str, pattern: str, step_by_step: bool = False):
        results = []
        for alg in self.algorithms:
            results.append(alg.search(text, pattern, step_by_step))
        return results

    def compare_performance(self, results):
        if not results:
            return {'fastest': None, 'least_comparisons': None}

        fastest = min(results, key=lambda x: x.get('time_ms', float('inf')))
        least = min(results, key=lambda x: x.get('comparisons', float('inf')))

        return {
            'fastest': fastest,
            'least_comparisons': least
        }