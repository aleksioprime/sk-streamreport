import { AuthResource } from "@/services/resources/auth.resource";
import { UserResource } from "@/services/resources/general/user.resource";
import { GroupResource } from "@/services/resources/general/group.resource";
import { AcademicYearResource } from "@/services/resources/general/academicYear.resource";
import { ReportPeriodResource } from "@/services/resources/report/reportPeriod.resource";
import { StudentExtraReportResource } from "@/services/resources/report/studentExtraReport.resource";
import { ReportExtraResource } from "@/services/resources/report/reportExtra.resource";
import { ReportTeacherPrimaryResource } from "@/services/resources/report/reportTeacherPrimary.resource";
import { ReportTeacherSecondaryResource } from "@/services/resources/report/reportTeacherSecondary.resource";
import { ReportTeacherHighResource } from "@/services/resources/report/reportTeacherHigh.resource";
import { ReportPrimaryTopicResource } from "@/services/resources/report/reportPrimaryTopic.resource";
import { StudyYearResource } from "@/services/resources/general/studyYear.resource";
import { SubjectResource } from "@/services/resources/curriculum/subject.resource";
import { CurriculumResource } from "@/services/resources/curriculum/curriculum.resource";
import { CourseResource } from "@/services/resources/syllabus/course.resource";

export default {
    auth: new AuthResource(),
    user: new UserResource(),
    group: new GroupResource(),
    academicYear: new AcademicYearResource(),
    reportPeriod: new ReportPeriodResource(),
    studentExtraReport: new StudentExtraReportResource(),
    reportExtra: new ReportExtraResource(),
    reportTeacherPrimary: new ReportTeacherPrimaryResource(),
    reportTeacherSecondary: new ReportTeacherSecondaryResource(),
    reportTeacherHigh: new ReportTeacherHighResource(),
    reportPrimaryTopic: new ReportPrimaryTopicResource(),
    studyYear: new StudyYearResource(),
    subject: new SubjectResource(),
    curriculum: new CurriculumResource(),
    course: new CourseResource(),
  };