# data_pipeline.py
# A simple data processing pipeline for marketing campaign metrics

import json


def load_campaign_data(filepath):
    f = open(filepath, 'r')
    data = json.load(f)
    return data


def calculate_roas(revenue, spend):
    return revenue / spend


def calculate_cpa(spend, conversions):
    return spend / conversions


def get_top_campaigns(campaigns, metric, n=5):
    sorted_campaigns = sorted(campaigns, key=lambda x: x[metric], reverse=True)
    return sorted_campaigns[:n]


def summarize_campaigns(campaigns):
    total_spend = 0
    total_revenue = 0
    total_conversions = 0
    total_impressions = 0

    for c in campaigns:
        total_spend += c['spend']
        total_revenue += c['revenue']
        total_conversions += c['conversions']
        total_impressions += c['impressions']

    summary = {
        'total_spend': total_spend,
        'total_revenue': total_revenue,
        'total_conversions': total_conversions,
        'total_impressions': total_impressions,
        'overall_roas': calculate_roas(total_revenue, total_spend),
        'overall_cpa': calculate_cpa(total_spend, total_conversions),
        'ctr': total_conversions / total_impressions
    }
    return summary


def filter_campaigns(campaigns, min_spend=None, max_cpa=None, channel=None):
    results = []
    for c in campaigns:
        if min_spend and c['spend'] < min_spend:
            continue
        if max_cpa and calculate_cpa(c['spend'], c['conversions']) > max_cpa:
            continue
        if channel and c['channel'] != channel:
            continue
        results.append(c)
    return results


def generate_report(filepath):
    data = load_campaign_data(filepath)
    campaigns = data['campaigns']

    summary = summarize_campaigns(campaigns)
    top_by_roas = get_top_campaigns(campaigns, 'revenue')

    report = "CAMPAIGN PERFORMANCE REPORT\n"
    report += "=" * 40 + "\n"
    report += f"Total Spend: ${summary['total_spend']}\n"
    report += f"Total Revenue: ${summary['total_revenue']}\n"
    report += f"Overall ROAS: {summary['overall_roas']}\n"
    report += f"Overall CPA: ${summary['overall_cpa']}\n"
    report += f"CTR: {summary['ctr']}%\n"
    report += "\nTOP CAMPAIGNS:\n"
    for c in top_by_roas:
        report += f"  - {c['name']}: ${c['revenue']} revenue\n"

    print(report)
    return report
