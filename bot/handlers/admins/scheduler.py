from typing import List

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from filters.is_admin import IsAdmin


router = Router()


@router.message(IsAdmin(), Command("jobs"))
async def handle_jobs_command(
    message: Message, scheduler: AsyncIOScheduler
) -> None:
    """Handles the /jobs command."""
    jobs: List[Job] = scheduler.get_jobs()
    text = ""
    for job in jobs:
        text += (
            f"🆔 <code>{job.id}</code> ({job.name})\n"
            f"📅 {job.trigger} ({job.next_run_time.strftime('%d.%m.%Y %H:%M')})\n\n"
        )
    await message.answer(text or "No jobs found.")


@router.message(IsAdmin(), Command("job"))
async def handle_job_command(
    message: Message, scheduler: AsyncIOScheduler
) -> None:
    """Handles the /job command."""
    try:
        job_id = message.text.split(" ")[1]
    except (ValueError, IndexError):
        await message.answer("Invalid command usage.")
        return
    job = scheduler.get_job(job_id)
    if job is None:
        return await message.answer("Job not found.")
    text = (
        f"🆔 <code>{job.id}</code>\n"
        f"📝 {job.name}\n"
        f"📅 {job.trigger} ({job.next_run_time.strftime('%d.%m.%Y %H:%M')})\n\n"
        f"🔧 {job.args}\n"
        f"🔧 {job.kwargs}"
    )
    await message.answer(text)
