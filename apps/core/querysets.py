from typing import Generic, Literal, TypeVar

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.functions import Coalesce

T = TypeVar("T")


class EmployeesCountQuerysetMixin(Generic[T]):
    def annotate_employees_count(self) -> T:
        return self.annotate(
            employees_count=models.Count("employees", distinct=True),
        )


class EmployeesCountManagerMixin(Generic[T]):
    def annotate_employees_count(self) -> T:
        return self.get_queryset().annotate_employees_count()


class JournalsTotalsQuerysetMixin(Generic[T]):
    def _annotate_journals_total_field(
        self,
        field_name: Literal["debit", "credit", "amount"],
        sum_filter_Q: models.Q | None = None,
        filter_compensations: bool = True,
    ) -> T:
        """
        Returns a queryset annotated with totals from their journals.
        """

        q = models.Q()

        if filter_compensations:
            compensation_ct = ContentType.objects.get_by_natural_key(
                "fin", "compensation"
            )
            q &= models.Q(journals__content_type=compensation_ct)

        sum_obj = models.Sum(f"journals__{field_name}", filter=q)

        if sum_filter_Q:
            sum_obj = models.Sum(
                f"journals__{field_name}",
                filter=sum_filter_Q & q,
            )

        return self.annotate(
            **{
                f"total_{field_name}": Coalesce(
                    sum_obj,
                    0,
                    output_field=models.DecimalField(
                        max_digits=20,
                        decimal_places=4,
                    ),
                )
            },
        )

    def annotate_journals_total_debit(
        self,
        sum_filter_Q: models.Q | None = None,
        filter_compensations: bool = True,
    ):
        return self._annotate_journals_total_field(
            "debit", sum_filter_Q, filter_compensations
        )

    def annotate_journals_total_credit(
        self,
        sum_filter_Q: models.Q | None = None,
        filter_compensations: bool = True,
    ):
        return self._annotate_journals_total_field(
            "credit", sum_filter_Q, filter_compensations
        )

    def annotate_journals_total_amount(
        self,
        sum_filter_Q: models.Q | None = None,
        filter_compensations: bool = True,
    ):
        return self._annotate_journals_total_field(
            "amount", sum_filter_Q, filter_compensations
        )


class JournalsTotalsManagerMixin(Generic[T]):
    def annotate_journals_total_debit(
        self,
        sum_filter_Q: models.Q | None = None,
        filter_compensations: bool = True,
    ) -> T:
        return self.get_queryset().annotate_journals_total_debit(
            sum_filter_Q, filter_compensations
        )

    def annotate_journals_total_credit(
        self,
        sum_filter_Q: models.Q | None = None,
        filter_compensations: bool = True,
    ) -> T:
        return self.get_queryset().annotate_journals_total_credit(
            sum_filter_Q, filter_compensations
        )

    def annotate_journals_total_amount(
        self,
        sum_filter_Q: models.Q | None = None,
        filter_compensations: bool = True,
    ) -> T:
        return self.get_queryset().annotate_journals_total_amount(
            sum_filter_Q, filter_compensations
        )
