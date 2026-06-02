import argparse
import subprocess
from datetime import datetime
from pathlib import Path
import pandas as pd

# Caminho para o executável do JMeter
JMETER_PATH = r"D:\Users\RaFa\Desktop\apache-jmeter-5.6.3\bin\jmeter.bat"

# Arquivos
TEST_PLAN = "testes1.jmx"
RESULTS_DIR = Path("resultados")

def gerar_arquivo_resultado(usuarios: int, rampup: int, loops: int) -> Path:
    RESULTS_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome = f"resultado_u{usuarios}_r{rampup}_l{loops}_{timestamp}.jtl"
    return RESULTS_DIR / nome

def executar_teste(usuarios: int, rampup: int, loops: int, result_file: Path):
    comando = [
        JMETER_PATH,
        "-n",
        "-t", TEST_PLAN,
        "-l", str(result_file),
        f"-Jthreads={usuarios}",
        f"-Jrampup={rampup}",
        f"-Jloops={loops}",
    ]

    print(f"Executando teste: {usuarios} usuário(s), ramp-up {rampup}s, {loops} loop(s)...")
    print(f"Salvando resultados em: {result_file}")

    resultado = subprocess.run(
        comando,
        capture_output=True,
        text=True
    )

    print(resultado.stdout)

    if resultado.returncode != 0:
        print(resultado.stderr)
        raise Exception("Falha na execução do JMeter")

def analisar_resultados(result_file: Path):
    if not result_file.exists():
        raise FileNotFoundError(
            f"Arquivo {result_file} não encontrado."
        )

    df = pd.read_csv(result_file)

    tempos = df["elapsed"]

    total = len(df)
    sucesso = len(df[df["success"] == True])
    erros = total - sucesso

    df_erros = df[df["success"] == False]
    erros_agrupados = (
        df_erros
        .groupby(["responseCode", "responseMessage"])
        .size()
        .reset_index(name="ocorrencias")
        .sort_values("ocorrencias", ascending=False)
        .to_dict(orient="records")
    )

    metricas = {
        "total_requisicoes": total,
        "sucessos": sucesso,
        "erros": erros,
        "taxa_sucesso": round((sucesso / total) * 100, 2),
        "tempo_medio_ms": round(tempos.mean(), 2),
        "tempo_min_ms": int(tempos.min()),
        "tempo_max_ms": int(tempos.max()),
        "p95_ms": round(tempos.quantile(0.95), 2),
        "p99_ms": round(tempos.quantile(0.99), 2),
        "detalhes_erros": erros_agrupados,
    }

    return metricas

def imprimir_resultados(metricas: dict):
    print("\n=== RESULTADOS ===")
    for chave, valor in metricas.items():
        if chave == "detalhes_erros":
            continue
        print(f"{chave}: {valor}")

    detalhes = metricas.get("detalhes_erros", [])
    if detalhes:
        print("\n--- ERROS ENCONTRADOS ---")
        for erro in detalhes:
            print(
                f"  Código {erro['responseCode']} "
                f"({erro['responseMessage']}): "
                f"{erro['ocorrencias']} ocorrência(s)"
            )
    else:
        print("\nNenhum erro registrado.")

def main():
    parser = argparse.ArgumentParser(description="Executor de testes de desempenho com JMeter")
    parser.add_argument("--usuarios", type=int, default=1, help="Número de usuários simultâneos (threads)")
    parser.add_argument("--rampup",   type=int, default=1, help="Tempo de ramp-up em segundos")
    parser.add_argument("--loops",    type=int, default=1, help="Número de repetições por usuário")
    args = parser.parse_args()

    result_file = gerar_arquivo_resultado(args.usuarios, args.rampup, args.loops)

    executar_teste(
        usuarios=args.usuarios,
        rampup=args.rampup,
        loops=args.loops,
        result_file=result_file,
    )

    metricas = analisar_resultados(result_file)

    imprimir_resultados(metricas)

if __name__ == "__main__":
    main()