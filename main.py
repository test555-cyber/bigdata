import argparse
from datetime import datetime
from jobs.daily_index import DailyIndexJob
from jobs.history_backfill import HistoryBackfillJob


def main():
    parser = argparse.ArgumentParser(description='价格指数计算系统')
    subparsers = parser.add_subparsers(dest='command')

    # 每日任务命令
    daily_parser = subparsers.add_parser('daily', help='执行每日计算')
    daily_parser.add_argument('--date', type=str, help='指定处理日期(YYYY-MM-DD)')

    # 回填命令
    backfill_parser = subparsers.add_parser('backfill', help='历史数据回填')
    backfill_parser.add_argument('start_date', type=str, help='开始日期(YYYY-MM-DD)')
    backfill_parser.add_argument('end_date', type=str, help='结束日期(YYYY-MM-DD)')

    args = parser.parse_args()

    if args.command == 'daily':
        job = DailyIndexJob()
        if args.date:
            date = datetime.strptime(args.date, '%Y-%m-%d').date()
            job.run(date)
        else:
            job.run()

    elif args.command == 'backfill':
        job = HistoryBackfillJob()
        start_date = datetime.strptime(args.start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(args.end_date, '%Y-%m-%d').date()
        job.run(start_date, end_date)


if __name__ == "__main__":
    main()