import jakarta.persistence.*;
import java.util.Date;

@Entity
@Table(name = "INDIV", schema = "PARTYDBA")
public class Indiv {

    @Id
    @Column(name = "PARTY_ID", nullable = false)
    private Long partyId;

    @Column(name = "SSN", length = 9)
    private String ssn;

    @Column(name = "SSN_VAL_FLAG", length = 1)
    private String ssnValFlag;

    @Column(name = "NAME_PREFX", length = 4)
    private String namePrefix;

    @Column(name = "FIRST_NAME", length = 32, nullable = false)
    private String firstName;

    @Column(name = "LAST_NAME", length = 32, nullable = false)
    private String lastName;

    @Column(name = "MID_NAME", length = 32)
    private String midName;

    @Column(name = "NAME_SUFFX", length = 5)
    private String nameSuffix;

    @Column(name = "DOB")
    private Date dob;

    @Column(name = "DEATH_TS")
    private Date deathTs;

    @Column(name = "INSRT_TS", nullable = false)
    private Date insertTs;

    @Column(name = "INSRT_USER", length = 64, nullable = false)
    private String insertUser;

    @Column(name = "FRNDLY_NAME", length = 32)
    private String friendlyName;

    @Column(name = "HHI")
    private Long hhi;

    @Column(name = "STMNT_CYCLE", length = 2)
    private String statementCycle;

    @Column(name = "MOD_TS")
    private Date modTs;

    @Column(name = "MOD_USER", length = 64)
    private String modUser;

    @Column(name = "INVAL_RGSTR_ATMPT_COUNT")
    private Long invalidRegisterAttemptCount;

    @Column(name = "FIRST_RGSTR_ATMPT_IN_LAST24HRS")
    private Date firstRegisterAttemptInLast24Hrs;

    @Column(name = "CNTRY_CTZN_CD", length = 10)
    private String countryCitizenCode;

    @Column(name = "ANNL_INCME_RPT_DT")
    private Date annualIncomeReportDate;

    @Column(name = "ANNL_INCME_RPT_SRC_CD", length = 50)
    private String annualIncomeReportSourceCode;

    @Column(name = "LAST_PRFLE_UPDT_DT")
    private Date lastProfileUpdateDate;

    @Column(name = "PTY_INDIV_TYPE_CD", length = 50)
    private String partyIndividualTypeCode;

    @Column(name = "ITIN", length = 20)
    private String itin;

    @Column(name = "CNTRY_RSDNCE_CD", length = 10)
    private String countryResidenceCode;

    @Column(name = "CUST_DCESD_CD", length = 50)
    private String customerDeceasedCode;

    @Column(name = "BNKRP_TYPE_CD", length = 100)
    private String bankruptcyTypeCode;

    @Column(name = "CIP_EXCPT_FLAG", length = 1)
    private String cipExceptionFlag;

    @Column(name = "PTY_REL_STRT_DT")
    private Date partyRelationshipStartDate;

    @Column(name = "PTY_STATUS_CD", length = 10)
    private String partyStatusCode;

    // Getters and setters (can be auto-generated using your IDE)

    public Long getPartyId() {
        return partyId;
    }

    public void setPartyId(Long partyId) {
        this.partyId = partyId;
    }

    public String getSsn() {
        return ssn;
    }

    public void setSsn(String ssn) {
        this.ssn = ssn;
    }

    public String getSsnValFlag() {
        return ssnValFlag;
    }

    public void setSsnValFlag(String ssnValFlag) {
        this.ssnValFlag = ssnValFlag;
    }

    // Add other getters and setters...
}