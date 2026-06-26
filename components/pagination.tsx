interface Props {
  page: number;
  totalPages: number;
  onPageChange: (page: number) => void;
}

export default function Pagination({
  page,
  totalPages,
  onPageChange,
}: Props) {

  return (

    <div className="flex justify-center gap-3 mt-10">

      <button
        disabled={page === 1}
        onClick={() =>
          onPageChange(page - 1)
        }
        className="px-5 py-2 rounded-xl bg-white/10 text-white disabled:opacity-40"
      >
        Previous
      </button>

      {Array.from(
        { length: totalPages },
        (_, i) => (

          <button
            key={i}
            onClick={() =>
              onPageChange(i + 1)
            }
            className={`px-4 py-2 rounded-xl ${
              page === i + 1
                ? "bg-cyan-500"
                : "bg-white/10"
            }`}
          >
            {i + 1}
          </button>

        )
      )}

      <button
        disabled={page === totalPages}
        onClick={() =>
          onPageChange(page + 1)
        }
        className="px-5 py-2 rounded-xl bg-white/10 text-white disabled:opacity-40"
      >
        Next
      </button>

    </div>

  );

}