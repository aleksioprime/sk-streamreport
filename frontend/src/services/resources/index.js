import { AuthResource } from "@/services/resources/auth.resource";
import { UserResource } from "@/services/resources/general/user.resource";
import { GroupResource } from "@/services/resources/general/group.resource";
import { AcademicYearResource } from "@/services/resources/general/academicYear.resource";
import { ReportPeriodResource } from "@/services/resources/report/reportPeriod.resource";
import { StudentExtraReportResource } from "@/services/resources/report/studentExtraReport.resource";
import { StudyYearResource } from "@/services/resources/general/studyYear.resource";
import { SubjectResource } from "@/services/resources/subject.resource";

export default {
    auth: new AuthResource(),
    user: new UserResource(),
    group: new GroupResource(),
    academicYear: new AcademicYearResource(),
    reportPeriod: new ReportPeriodResource(),
    studentExtraReport: new StudentExtraReportResource(),
    studyYear: new StudyYearResource(),
    subject: new SubjectResource(),
  };